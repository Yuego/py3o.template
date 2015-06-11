# -*- encoding: utf-8 -*-
from py3o.template.data_struct import Py3oDataError
from py3o.template.helpers import Py3oConvertor

import unittest
import os

import lxml.etree
import pkg_resources
import six

from pyjon.utils import get_secure_filename

from py3o.template.main import move_siblings, detect_keep_boundary, Template, \
    get_soft_breaks

if six.PY3:
    # noinspection PyUnresolvedReferences
    from unittest.mock import Mock
elif six.PY2:
    # noinspection PyUnresolvedReferences
    from mock import Mock


class TestHelpers(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        template_name = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/py3o_example_template.odt'
        )

        outname = get_secure_filename()

        self.reference_template = Template(template_name, outname)
        os.unlink(outname)

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

        expected_result = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_two_result.xml'
            )
        ).read()

        expected_result = expected_result.replace(
            '\n', '').replace(' ', '').strip()

        result_s = result_s.replace('\n', '').replace(' ', '').strip()

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

        move_siblings(
            start, end, new_,
            keep_start_boundary=True,
            keep_end_boundary=True,
        )

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

        move_siblings(
            start, end, new_,
            keep_start_boundary=True,
            keep_end_boundary=True,
        )

        result_s = lxml.etree.tostring(
            test_template_four,
            pretty_print=True,
        ).decode('utf-8')

        expected_result = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_four_result.xml'
            )
        ).read()

        expected_result = expected_result.replace(
            '\n', '').replace(' ', '').strip()

        result_s = result_s.replace('\n', '').replace(' ', '').strip()

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
            'line.val1',
            'line.val2',
            'line.val3',
            'item.Amount',
            'item.Currency',
            'item.InvoiceRef',
            'document.total',
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
        assert set(user_instructions) == set(expected_vars)

    def test_detect_boundary_false(self):
        """boundary detection should say no!!"""

        source_xml_filename = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/keepboundary_detection_false.xml'
        )

        test_xml = lxml.etree.parse(source_xml_filename)
        starts, ends = self.reference_template.find_instructions(
            [test_xml], self.reference_template.namespaces
        )
        for start, base in starts:
            end = ends[id(start)]
            keep_start, keep_end = detect_keep_boundary(
                start, end,  self.reference_template.namespaces
            )
            assert keep_start is False
            assert keep_end is False

    def test_detect_boundary_true(self):
        """boundary detection should say yes!!"""

        source_xml_filename = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/keepboundary_detection_true.xml'
        )

        test_xml = lxml.etree.parse(source_xml_filename)
        starts, ends = self.reference_template.find_instructions(
            [test_xml], self.reference_template.namespaces
        )
        for index, (start, base) in enumerate(starts):
            end = ends[id(start)]
            keep_start, keep_end = detect_keep_boundary(
                start, end,  self.reference_template.namespaces
            )
            if index == 0:
                assert keep_start is False
                assert keep_end is True

            else:
                assert False, "We should find one single link"

    def test_move_siblings_1(self):
        template_xml = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/move_siblings.xml'
        )
        test_xml = lxml.etree.parse(template_xml)
        starts, ends = self.reference_template.find_instructions(
            [test_xml], self.reference_template.namespaces
        )

        assert len(starts) == 1
        assert len(ends) == 1

        start, _ = starts[0]
        end = ends[id(start)]

        keep_start, keep_end = detect_keep_boundary(
            start, end,  self.reference_template.namespaces
        )

        assert keep_start is True
        assert keep_end is False

        new_ = lxml.etree.Element('finishcontainer')

        start_parent = start.getparent()
        end_parent = end.getparent()

        start.getparent().remove(start)
        end.getparent().remove(end)

        move_siblings(
            start_parent, end_parent, new_,
            keep_start_boundary=keep_start,
            keep_end_boundary=keep_end,
        )

        result_a = lxml.etree.tostring(
            test_xml,
            pretty_print=True,
        ).decode('utf-8')

        result_e = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_siblings_result_1.xml'
            )
        ).read()

        result_a = result_a.replace("\n", "").replace(" ", "")
        result_e = result_e.replace("\n", "").replace(" ", "")

        assert result_a == result_e

    def test_move_siblings_2(self):
        template_xml = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/move_siblings.xml'
        )
        test_xml = lxml.etree.parse(template_xml)
        starts, ends = self.reference_template.find_instructions(
            [test_xml], self.reference_template.namespaces
        )

        assert len(starts) == 1
        assert len(ends) == 1

        start, base = starts[0]
        end = ends[id(start)]

        keep_start, keep_end = detect_keep_boundary(
            start, end,  self.reference_template.namespaces
        )

        assert keep_start is True
        assert keep_end is False

        self.reference_template.handle_link(start, base, end)
        result_a = lxml.etree.tostring(
            test_xml,
            pretty_print=True,
        ).decode('utf-8')

        result_e = open(
            pkg_resources.resource_filename(
                'py3o.template',
                'tests/templates/move_siblings_result_2.xml'
            )
        ).read()

        result_a = result_a.replace("\n", "").replace(" ", "")
        result_e = result_e.replace("\n", "").replace(" ", "")

        assert result_a == result_e

    def test_content_tree_with_child_instruction(self):
        template_xml = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/py3o_example_invalid_template.odt'
        )
        t = Template(template_xml, get_secure_filename())
        usr_insts = t.get_user_instructions()
        assert usr_insts == ['for="item in items"', '/for',
                             'for="item in items', '2', '"', '/for']

    def test_remove_soft_page_breaks(self):
        template_xml = pkg_resources.resource_filename(
            'py3o.template',
            'tests/templates/py3o_soft_page_break.odt'
        )
        t = Template(template_xml, get_secure_filename())
        soft_breaks = get_soft_breaks(t.content_trees[0], t.namespaces)
        assert len(soft_breaks) > 0

        t.remove_soft_breaks()
        soft_breaks = get_soft_breaks(t.content_trees[0], t.namespaces)
        assert len(soft_breaks) == 0

        t = Template(template_xml, get_secure_filename())
        soft_breaks = get_soft_breaks(t.content_trees[0], t.namespaces)
        assert len(soft_breaks) > 0

        t.render(data={"list1": [1, 2, 3]})
        soft_breaks = get_soft_breaks(t.content_trees[0], t.namespaces)
        assert len(soft_breaks) == 0

    def __load_and_convert_template(self, path):
        template_xml = pkg_resources.resource_filename(
            'py3o.template',
            path
        )
        t = Template(template_xml, get_secure_filename())
        expressions = t.get_all_user_python_expression()
        py_expr = t.convert_py3o_to_python_ast(expressions)
        return py_expr

    def test_access_global_variable_inside_loop(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/py3o_access_global_variable_inside_loop.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'global_var': Mock(val=1),
            'my4list': [0, 1, 2, 3],
        }
        json_str = res.render(user_data)
        assert json_str == {'global_var': {'val': 1}}

    def test_access_in_loop_variable(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/py3o_access_in_loop_variable.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'my2list': [0, 1, 2, 3, 4]
        }
        json_str = res.render(user_data)
        assert json_str == {'my2list': [0, 1, 2, 3, 4]}

    def test_iterable_with_global_attribute(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/py3o_iterable_with_global_attribute.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'foo': Mock(my2list=[0, 1, 2, 3, 4])
        }
        json_str = res.render(user_data)
        assert json_str == {'foo': {'my2list': [0, 1, 2, 3, 4]}}

    def test_two_for_list_on_same_attribute(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/py3o_two_for_list_on_same_attribute.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'foo': Mock(
                my2list=[0, 1, 2, 3, 4],
                my3list=[5, 6, 7, 8],
            )
        }
        json_str = res.render(user_data)
        assert json_str == {
            'foo': {
                'my2list': [0, 1, 2, 3, 4],
                'my3list': [5, 6, 7, 8],
            }
        }

    def test_access_in_loop_variable_with_attribute(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/py3o_access_in_loop_variable_with_attribute.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'my3list': [
                Mock(val=0),
                Mock(val=1),
                Mock(val=2),
            ]
        }
        json_str = res.render(user_data)
        assert json_str == {
            'my3list': [
                {'val': 0},
                {'val': 1},
                {'val': 2},
            ]
        }

    def test_access_in_loop_variable_with_multiple_attribute(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/'
            'py3o_access_in_loop_variable_with_multiple_attribute.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'my3list': [
                Mock(foo=Mock(val=0)),
                Mock(foo=Mock(val=1)),
                Mock(foo=Mock(val=2)),
            ]
        }
        json_str = res.render(user_data)
        assert json_str == {
            'my3list': [
                {'foo': {'val': 0}},
                {'foo': {'val': 1}},
                {'foo': {'val': 2}},
            ]
        }

    def test_access_parent_variable_in_nested_loop(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/py3o_access_parent_variable_in_nested_loop.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'my9list': [Mock(val=10), Mock(val=11)]
        }
        json_str = res.render(user_data)
        assert json_str == {
            'my9list': [
                {'val': 10},
                {'val': 11},
            ]
        }

    def test_access_parent_variable_in_nested_loop_with_attribute(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/'
            'py3o_access_parent_variable_in_nested_loop_with_attribute.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'my10list': [
                Mock(my_list=[
                    Mock(val=10),
                    Mock(val=11),
                ]),
                Mock(my_list=[
                    Mock(val=20),
                    Mock(val=21),
                    Mock(val=22),
                ]),
            ]
        }
        json_str = res.render(user_data)
        assert json_str == {
            'my10list': [
                {'my_list': [
                    {'val': 10},
                    {'val': 11},
                ]},
                {'my_list': [
                    {'val': 20},
                    {'val': 21},
                    {'val': 22},
                ]},
            ]
        }

    def test_access_variable_in_nested_loop(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/'
            'py3o_access_variable_in_nested_loop.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {
            'my8list': [
                [10, 11, 12],
                [20, 21, 22, 23],
            ]
        }
        json_str = res.render(user_data)
        assert json_str == {
            'my8list': [
                [10, 11, 12],
                [20, 21, 22, 23]
            ]
        }

    def test_bad_user_data(self):
        py_expr = self.__load_and_convert_template(
            'tests/templates/py3o_access_global_variable_inside_loop.odt'
        )
        p = Py3oConvertor()
        res = p(py_expr)

        user_data = {}
        with self.assertRaises(Py3oDataError):
            res.render(user_data)
