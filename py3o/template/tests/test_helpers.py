# -*- encoding: utf-8 -*-
__author__ = 'faide'

import unittest

import lxml.etree
import pkg_resources

from pyjon.utils import get_secure_filename

from py3o.template.main import move_siblings, Template


class TestHelpers(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test_move_1(self):
        """test that siblings are properly moved without keeping boundaries"""
        template_one_name = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/move_one.xml'
        )
        test_template_one = lxml.etree.parse(template_one_name)
        start = test_template_one.find('mystruct/start')
        end = test_template_one.find('mystruct/end')
        new_ = lxml.etree.Element("finishcontainer")

        move_siblings(start, end, new_)

        result_s = lxml.etree.tostring(
            test_template_one,
            pretty_print=True,
        ).decode('utf-8')

        expected_result = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_one_result.xml'
            )
        ).read()

        expected_result = expected_result.replace(
            '\n', '').replace(' ', '').strip()

        result_s = result_s.replace('\n', '').replace(' ', '').strip()

        assert result_s == expected_result

    def test_move_2(self):
        """start.tail is correctly copied without keeping boundaries"""
        template_two_name = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/move_two.xml'
        )
        test_template_two = lxml.etree.parse(template_two_name)
        start = test_template_two.find('mystruct/start')
        end = test_template_two.find('mystruct/end')
        new_ = lxml.etree.Element('finishcontainer')

        move_siblings(start, end, new_)

        result_s = lxml.etree.tostring(
            test_template_two,
            pretty_print=True,
        ).decode('utf-8')

        print(type(result_s))

        expected_result = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_two_result.xml'
            )
        ).read()

        expected_result = expected_result.replace(
            '\n', '').replace(' ', '').strip()

        result_s = result_s.replace('\n', '').replace(' ', '').strip()

        print(result_s)

        assert result_s == expected_result

    def test_move_keep_boundaries(self):
        """test that siblings are properly moved keeping boundaries"""
        template_three_name = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/move_three.xml'
        )
        test_template_three = lxml.etree.parse(template_three_name)
        start = test_template_three.find('mystruct/start')
        end = test_template_three.find('mystruct/end')

        new_ = lxml.etree.Element('finishcontainer')

        move_siblings(start, end, new_, keep_boundaries=True)

        result_s = lxml.etree.tostring(
            test_template_three,
            pretty_print=True,
        ).decode('utf-8')

        expected_result = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_three_result.xml'
            )
        ).read()

        expected_result = expected_result.replace(
            '\n', '').replace(' ', '').strip()

        result_s = result_s.replace('\n', '').replace(' ', '').strip()

        assert result_s == expected_result

    def test_move_2_keep_boundaries(self):
        """test that start.tail is correctly copied keeping boundaries"""
        template_four_name = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/move_four.xml'
        )
        test_template_four = lxml.etree.parse(template_four_name)
        start = test_template_four.find('mystruct/start')
        end = test_template_four.find('mystruct/end')

        new_ = lxml.etree.Element('finishcontainer')

        move_siblings(start, end, new_, keep_boundaries=True)

        result_s = lxml.etree.tostring(
            test_template_four,
            pretty_print=True,
        ).decode('utf-8')

        print(type(result_s))

        expected_result = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_four_result.xml'
            )
        ).read()

        expected_result = expected_result.replace(
            '\n', '').replace(' ', '').strip()

        result_s = result_s.replace('\n', '').replace(' ', '').strip()

        print(result_s)

        assert result_s == expected_result

    def test_get_user_variables(self):
        source_odt_filename = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/py3o_example_template.odt'
        )
        outfilename = get_secure_filename()

        template = Template(source_odt_filename, outfilename)

        user_vars = template.get_user_variables()

        expected_vars = [
            'py3o.line.val1',
            'py3o.line.val2',
            'py3o.line.val3',
            'py3o.item.Amount',
            'py3o.item.Currency',
            'py3o.item.InvoiceRef',
            'py3o.document.total',
        ]
        assert set(user_vars) == set(expected_vars)

    def test_get_user_instructions(self):
        source_odt_filename = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/py3o_example_template.odt'
        )
        outfilename = get_secure_filename()

        template = Template(source_odt_filename, outfilename)

        user_instructions = template.get_user_instructions()

        expected_vars = [
            'for="line in items"',
            '/for',
            'for="item in items"',
            'if="item.InvoiceRef==\'#1234\'"',
            '/if',
            '/for',
        ]
        print(user_instructions)
        assert set(user_instructions) == set(expected_vars)
