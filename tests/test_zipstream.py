# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import tempfile
import unittest
import zipstream
import zipfile
import socket


class ZipInfoTestCase(unittest.TestCase):
    pass


class ZipStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.fileobjs = [
            tempfile.NamedTemporaryFile(delete=False, suffix='.txt'),
            tempfile.NamedTemporaryFile(delete=False, suffix='.py'),
        ]

    def tearDown(self):
        for fileobj in self.fileobjs:
            fileobj.close()
            os.remove(fileobj.name)

    def test_init_no_args(self):
        zipstream.ZipFile()

    def test_init_mode(self):
        try:
            zipstream.ZipFile(mode='w')
        except Exception as err:
            self.fail(err)

        for mode in ['wb', 'r', 'rb', 'a', 'ab']:
            self.assertRaises(Exception, zipstream.ZipFile, mode=mode)

        for mode in ['wb', 'r', 'rb', 'a', 'ab']:
            self.assertRaises(Exception, zipstream.ZipFile, mode=mode + '+')

    def test_write_file(self):
        z = zipstream.ZipFile(mode='w')
        for fileobj in self.fileobjs:
            z.write(fileobj.name)

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        z2.testzip()

        os.remove(f.name)

    def test_write_fp(self):
        z = zipstream.ZipFile(mode='w')
        for fileobj in self.fileobjs:
            z.write(fileobj)

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        z2.testzip()

        os.remove(f.name)

    @unittest.skipUnless(os.name == "posix", "requires POSIX")
    def test_write_socket(self):
        z = zipstream.ZipFile(mode='w')
        s, c = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            txt = "FILE CONTENTS"
            s.send(txt.encode("utf-8"))
            z.write(c.makefile())
            s.close()

            f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
            for chunk in z:
                f.write(chunk)
            f.close()

            z2 = zipfile.ZipFile(f.name, 'r')
            z2.testzip()

            os.remove(f.name)
        finally:
            c.close()


if __name__ == '__main__':
    unittest.main()