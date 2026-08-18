# -*- coding: utf-8 -*-
"""Page Object 模式 - 页面对象层"""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.score_page import ScorePage

__all__ = ["BasePage", "LoginPage", "ScorePage"]
