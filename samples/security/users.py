#!/usr/bin/env python

# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


# A basic OpenSearch sample that create and manage users.

from opensearchpy import OpenSearch

# connect to OpenSearch

host = "localhost"
port = 9200
auth = ("admin", "admin")  # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
)

# Create a User

user_name = "test-user"
user_content = {"password": "opensearch@123", "opendistro_security_roles": []}

response = client.security.create_user(user_name, body=user_content)
print(response)

# Get a User

user_name = "test-user"

response = client.security.get_user(user_name)
print(response)
