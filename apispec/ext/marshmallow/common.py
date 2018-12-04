# -*- coding: utf-8 -*-
"""Utilities to get schema instances/classes"""

import copy
from collections import namedtuple

import marshmallow


MODIFIERS = ['only', 'exclude', 'load_only', 'dump_only', 'partial']


def resolve_schema_instance(schema):
    """Return schema instance for given schema (instance or class)

    :param type|Schema|str schema: instance, class or class name of marshmallow.Schema
    :return: schema instance of given schema (instance or class)
    """
    if isinstance(schema, type) and issubclass(schema, marshmallow.Schema):
        return schema()
    if isinstance(schema, marshmallow.Schema):
        return schema
    return marshmallow.class_registry.get_class(schema)()


def resolve_schema_cls(schema):
    """Return schema class for given schema (instance or class)

    :param type|Schema|str: instance, class or class name of marshmallow.Schema
    :return: schema class of given schema (instance or class)
    """
    if isinstance(schema, type) and issubclass(schema, marshmallow.Schema):
        return schema
    if isinstance(schema, marshmallow.Schema):
        return type(schema)
    return marshmallow.class_registry.get_class(schema)


def get_fields(schema):
    """Return fields from schema"""
    if hasattr(schema, 'fields'):
        return schema.fields
    elif hasattr(schema, '_declared_fields'):
        return copy.deepcopy(schema._declared_fields)
    raise ValueError("{0!r} doesn't have either `fields` or `_declared_fields`".format(schema))


def make_schema_key(schema):
    if not isinstance(schema, marshmallow.Schema):
        raise TypeError('can only make a schema key based on a Schema instance')
    modifiers = []
    for modifier in MODIFIERS:
        attribute = getattr(schema, modifier)
        try:
            hash(attribute)
        except TypeError:
            attribute = tuple(attribute)
        modifiers.append(attribute)
    return SchemaKey(schema.__class__, *modifiers)


SchemaKey = namedtuple('SchemaKey', ['SchemaClass'] + MODIFIERS)
