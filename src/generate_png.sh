#!/bin/sh

# Copyright 2020 VMware, Inc.
# SPDX-License-Identifier: BSD-2-Clause

# generate a png from document.py
# requires pyreverse and graphviz
pyreverse document.py && dot -Tpng classes.dot -o $1 && rm classes.dot
