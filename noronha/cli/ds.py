# -*- coding: utf-8 -*-

import click
import os

from noronha.api.ds import DatasetAPI as API
from noronha.cli.callback import ListingCallback
from noronha.cli.handler import CMD
from noronha.common.utils import assert_dict


@click.group()
def ds():
    
    """Datasets management"""


@click.command()
@click.option('--model', required=True, help="Name of the model to which this dataset belongs")
@click.option('--name', help="Name of the dataset")
def info(**kwargs):
    
    """Information about a dataset"""
    
    CMD.run(API, 'info', **kwargs)


@click.command()
@click.option('--model', required=True, help="Name of the model to which this dataset belongs")
@click.option('--name', help="Name of the dataset")
def rm(**kwargs):
    
    """Remove a dataset and all of its files"""
    
    CMD.run(API, 'rm', **kwargs)


@click.command('list')
@click.option('--filter', '-f', '_filter', help="Query in MongoDB's JSON syntax")
@click.option('--expand', '-e', default=False, is_flag=True, help="Flag: expand each record's fields")
@click.option('--model', help="Only datasets that belong to this model will be listed")
def _list(_filter, expand, **kwargs):
    
    """List datasets"""
    
    CMD.run(
        API, 'lyst', **kwargs,
        _filter=assert_dict(_filter, allow_none=True),
        _response_callback=ListingCallback(obj_title='Dataset', obj_attr='name', expand=expand)
    )


@click.command()
@click.option('--name', '-n', help="Name of the dataset (defaults to a random name)")
@click.option(
    '--model', '-m', required=True,
    help="The model to which this dataset belongs (further info: nha model --help)"
)
@click.option('--details', '-d', help="JSON with any details related to the dataset")
@click.option(
    '--path', '-p',
    help="Path to the directory that contains the dataset files (default: current working directory)"
)
@click.option(
    '--compress', '-c', 'compressed', default=False, is_flag=True,
    help="Flag: compress all dataset files to a single tar.gz archive"
)
def new(details, path=None, **kwargs):
    
    """Add a new dataset"""
    
    CMD.run(
        API, 'new', **kwargs,
        path=path or os.getcwd(),
        details=assert_dict(details, allow_none=True)
    )


@click.command()
@click.option('--name', '-n', required=True, help="Name of the dataset you want to update")
@click.option(
    '--model', '-m', required=True,
    help="The model to which this dataset belongs (further info: nha model --help)"
)
@click.option('--details', '-d', help="JSON with details related to the dataset")
@click.option(
    '--path', '-p',
    help="Path to the directory that contains the dataset files (default: current working directory)"
)
@click.option(
    '--compress', '-c', 'compressed', default=False, is_flag=True,
    help="Flag: compress all dataset files to a single tar.gz archive"
)
def update(details, path, **kwargs):
    
    """Update a dataset's details or files"""
    
    CMD.run(
        API, 'update', **kwargs,
        path=path or os.getcwd(),
        details=assert_dict(details, allow_none=True)
    )


commands = [new, _list, rm, update, info]

for cmd in commands:
    ds.add_command(cmd)
