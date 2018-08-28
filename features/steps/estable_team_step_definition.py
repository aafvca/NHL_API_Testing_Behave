#!/usr/bin/python3
# -*- coding: utf-8 -*-

from behave import given, when, then

@given(u'I send a request to get the roster1')
def step_impl(context):
    print('Request roster 1')

@given(u'I send a request to get the roster2')
def step_impl(context):
    print('Request roster 2')

@when(u'I find the players in both seasons')
def step_impl(context):
    print('I find the players in both seasons')

@then(u'At least 10 players should be in both seasons')
def step_impl(context):
    print('At least 10 players should be in both seasons')


