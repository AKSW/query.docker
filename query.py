#!/usr/bin/env python3

import sys
import os
import argparse
from rdflib import Graph, ConjunctiveGraph

from rdflib import URIRef, Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLStore


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a query to an enpoint.')

    parser.add_argument('query_endpoint', help='The SPARQL 1.1 query endpoint')

    # this will automatically open the file
    parser.add_argument('query_file', type=open, help='The query to execute on the endpoint')

    parser.add_argument('-f', '--result_format', default=None,
        choices=['raw', 'turtle', 'nt', 'json'],
        help='The result format, turtle and nt (n-triples) for contruct queries and json for select')

    # defaults to stdout, which is opened as byte system, which is required by rdflib of rdflib is updated use sys.stdout directly
    parser.add_argument('-t', '--target_file', default=os.fdopen(sys.stdout.fileno(), 'wb'),
        help='The target of the serialization. (default: stdout)')

    parser.add_argument('-g', '--graph', default=None,
        help='The graph to query. (default: none)')

    args = parser.parse_args()

    # Currently we use a Graph with SPARQLStore
    # We could also use the SPARQLStore directly or even the SPARQLConnector

    graph = Graph("SPARQLStore", identifier=args.graph)
    graph.open(args.query_endpoint)

    query_string = args.query_file.read()
    result = graph.query(query_string)

    if args.result_format:
        if args.result_format == "raw":
            result.serialize(destination=args.target_file)
        else:
            result.serialize(destination=args.target_file, format=args.result_format)
