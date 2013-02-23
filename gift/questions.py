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

class Question(object):
    def __init__(self, title, text):
        self.title = title
        self.text = text
    
    def answers(self):
        return ''
    
    def __str__(self):
        title = ''
        if self.title:
            title = '::%s:: ' % self.title
        
        return title + '%s {%s}' % (self.text, self.answers())

