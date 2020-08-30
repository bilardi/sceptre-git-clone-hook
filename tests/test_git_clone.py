# -*- coding: utf-8 -*-

import pytest
from mock import MagicMock
import subprocess, os, shutil

from hook.hook import GitClone
from sceptre.stack import Stack

class TestGitClone(object):
    repository='https://github.com/bilardi/sceptre-git-clone-hook'
    folder='my-folder'

    def setup_method(self, test_method):
        self.stack = MagicMock(spec=Stack)
        self.git_clone = GitClone(None, self.stack)

    def run_git_clone(self, argument, sceptre_user_data):
        self.git_clone.argument = argument
        self.git_clone.stack.sceptre_user_data = sceptre_user_data
        self.git_clone.run()
        response = os.path.exists(self.folder)
        shutil.rmtree(self.folder)
        assert response == True

    def run_with_argument(self):
        self.run_git_clone('{} {}'.format(self.repository, self.folder), None)

    def run_with_sceptre_user_data(self):
        self.run_git_clone(None, {'GitRepository':self.repository, 'RepositoryFolder': self.folder})

    def test_run_with_argument_and_sceptre_user_data(self):
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)

        # if there is self.argument, git_clone uses its details instead of that of self.stack.sceptre_user_data
        self.run_git_clone('{} {}'.format(self.repository, self.folder), {'GitRepository':'git:fake', 'RepositoryFolder': 'my-fake-folder'})

    def test_run_with_argument_without_folder(self):
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        self.run_with_argument()

    def test_run_with_sceptre_user_data_without_folder(self):
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        self.run_with_sceptre_user_data()

    def test_run_with_argument_with_folder(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        self.run_with_argument()

    def test_run_with_sceptre_user_data_with_folder(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        self.run_with_sceptre_user_data()

    def test_run_exception_nothing(self):
        with pytest.raises(Exception):
            self.run_git_clone(None, None)

    def test_run_exception_no_repository(self):
        with pytest.raises(Exception):
            self.run_git_clone('{}'.format(self.folder), None)
        with pytest.raises(Exception):
            self.run_git_clone(None, {'RepositoryFolder': self.folder})

    def test_run_exception_no_folder(self):
        with pytest.raises(Exception):
            self.run_git_clone('{}'.format(self.repository), None)
        with pytest.raises(Exception):
            self.run_git_clone(None, {'GitRepository':self.repository})

    def test_run_exception_with_repository_fake(self):
        with pytest.raises(Exception):
            self.run_git_clone('git://fake {}'.format(self.folder), None)
        with pytest.raises(Exception):
            self.run_git_clone(None, {'GitRepository':'git://fake', 'RepositoryFolder': self.folder})

    def test_run_exception_with_folder_fake(self):
        with pytest.raises(Exception):
            self.run_git_clone('{} {}'.format(self.repository, '/my/folder/fake'), None)
        with pytest.raises(Exception):
            self.run_git_clone(None, {'GitRepository':self.repository, 'RepositoryFolder': '/my/folder/fake'})
