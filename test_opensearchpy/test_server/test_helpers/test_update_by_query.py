# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from typing import Any

from opensearchpy.helpers.search import Q
from opensearchpy.helpers.update_by_query import UpdateByQuery


def test_update_by_query_no_script(write_client: Any, setup_ubq_tests: Any) -> None:
    index = setup_ubq_tests

    ubq = (
        UpdateByQuery(using=write_client)
        .index(index)
        .filter(~Q("exists", field="is_public"))
    )
    response = ubq.execute()

    assert response.total == 52
    assert response["took"] > 0
    assert not response.timed_out
    assert response.updated == 52
    assert response.deleted == 0
    assert response.took > 0
    assert response.success()


def test_update_by_query_with_script(write_client: Any, setup_ubq_tests: Any) -> None:
    index = setup_ubq_tests

    ubq = (
        UpdateByQuery(using=write_client)
        .index(index)
        .filter(~Q("exists", field="parent_shas"))
        .script(source="ctx._source.is_public = false")
    )
    ubq = ubq.params(conflicts="proceed")

    response = ubq.execute()
    assert response.total == 2
    assert response.updated == 2
    assert response.version_conflicts == 0


def test_delete_by_query_with_script(write_client: Any, setup_ubq_tests: Any) -> None:
    index = setup_ubq_tests

    ubq = (
        UpdateByQuery(using=write_client)
        .index(index)
        .filter(Q("match", parent_shas="1dd19210b5be92b960f7db6f66ae526288edccc3"))
        .script(source='ctx.op = "delete"')
    )
    ubq = ubq.params(conflicts="proceed")

    response = ubq.execute()

    assert response.total == 1
    assert response.deleted == 1
    assert response.success()
