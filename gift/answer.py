"""
This file is part of pygift.

pygift is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pygift is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pygift. If not, see <http://www.gnu.org/licenses/>.


Copyright (c) 2013 Vicente Ruiz <vruiz2.0@gmail.com>
"""
from abc import ABCMeta, abstractmethod
from gift.exceptions import *

class Answer(metaclass=ABCMeta):
    def __init__(self, feedback=None):
        self.feedback = self.escape(feedback or '')
    
    @abstractmethod
    def get_answer(self):
        """Genera el valor de la respuesta en formato GIFT"""
    
    def escape(self, text):
        return text # TODO: Special Characters ~ = # { }
    
    def __str__(self):
        feedback = '#%s' % self.feedback if self.feedback else ''
        return self.get_answer() + feedback

class NumericAnswer(Answer):
    def __str__(self):
        text = super().__str__()
        return '#' + text
    
    def get_numeric_value(self, value):
        # Primero intentamos convertirlo a entero
        try:
            value = int(value)
        except ValueError as e:
            # Si ocurre un error, lo intentamos convertir a decimal
            try:
                value = float(value)
            except ValueError as e:
                value = None
        
        return value

class MathAnswer(NumericAnswer):
    def __init__(self, answer, tolerance=None, feedback=None):
        super().__init__(feedback)
        self.answer = self.get_numeric_value(answer)
        self.tolerance = self.get_numeric_value(tolerance) if tolerance else 0.0
        if self.answer is None:
            raise MathAnswerValueError('Answer value must be numeric')
    
    def get_answer(self):
        tolerance = ':%s' % self.tolerance if self.tolerance else ''
        return '%s%s' % (self.answer, tolerance)

class MathRangeAnswer(NumericAnswer):
    def __init__(self, initial, final, feedback=None):
        super().__init__(feedback)
        self.initial = self.get_numeric_value(initial)
        self.final = self.get_numeric_value(final)
        if self.initial is None or self.final is None:
            raise MathAnswerValueError('Initial or final value is not numeric')
            
        if self.initial > self.final:
            raise MathAnswerValueError('Initial value must be less than final value')
    
    def get_answer(self):
        return '%s..%s' % (self.initial, self.final)


class TrueFalseAnswer(Answer):
    def __init__(self, answer, feedback=None):
        super().__init__(feedback)
        value_map = {
            'T': True,
            'TRUE': True,
            True: True,
            'F': False,
            'FALSE': False,
            False: False
        }
        try:
            self.answer = value_map[answer]
        except KeyError as e:
            raise TrueFalseValueError('This answer must be True or False')
    
    def get_answer(self):
        return 'T' if self.answer else 'F'


class ChoiceAnswer(Answer):
    def __init__(self, correct, text, percentage=None, tolerance=None, feedback=None):
        super().__init__(feedback)
        # Correct
        correct_map = {
            '=': '=',
            True: '=',
            '~': '~',
            False: '~'
        }
        try:
            self.correct = correct_map[correct]
        except KeyError as e:
            raise ChoiceAnswerValueError('This answer must be = or ~')
        # Text
        if not len(text):
            raise ChoiceAnswerValueError('This answer has not text')
        self.text = self.escape(text)
        # Percentage
        if percentage:
            try:
                percentage = int(percentage)
                if percentage < -100 or percentage > 100:
                    raise ChoiceAnswerValueError('Percentage must be between -100 and 100')
            except ValueError as e:
                raise ChoiceAnswerValueError('Percentage must be integer')
        self.percentage = percentage
        # Tolerance
        try:
            self.tolerance = float(tolerance) if tolerance else 0.0
        except ValueError as e:
            raise ChoiceAnswerValueError('Tolerance value must be numeric')
        
    def get_answer(self):
        percentage = '%%%s%%' % self.percentage if self.percentage else ''
        tolerance = ':%s' % self.tolerance if self.tolerance else ''
        return '%s%s%s%s' % (self.correct, percentage, self.text, tolerance)


class MatchingAnswer(Answer):
    """No soportan feedback ó percentageage"""
    
    def __init__(self, key, value):
        super().__init__()
        # Key
        if not len(key):
            raise MatchingAnswerValueError('This answer has not key')
        self.key = self.escape(key)
        # Value
        if not len(value):
            raise MatchingAnswerValueError('This answer has not value')
        self.value = self.escape(value)
        
    def get_answer(self):
        return '%s -> %s' % (self.key, self.value)
