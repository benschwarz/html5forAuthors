# coding=UTF-8
# Copyright (c) 2008 Geoffrey Sneddon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import glob
import StringIO
import os
import unittest

from anolislib import generator


def get_files(*args):
    return glob.glob(os.path.join(*args))


class TestCase(unittest.TestCase):
    pass


def buildTestSuite():
    for file_name in get_files("tests", "basic", "*.src.html"):

        def testFunc(self, file_name=file_name):
            try:
                # Get the input
                input = open(file_name, "rb")
                tree = generator.fromFile(input)
                input.close()

                # Get the output
                output = StringIO.StringIO()
                generator.toFile(tree, output)

                # Get the expected result
                expected = open(file_name[:-9] + ".html", "rb")

                # Run the test
                self.assertEquals(output.getvalue(), expected.read())

                # Close the files
                output.close()
                expected.close()
            except IOError, err:
                self.fail(err)

        setattr(TestCase, "test_%s" % (file_name), testFunc)


def main():
    buildTestSuite()
    unittest.main()

if __name__ == "__main__":
    main()
