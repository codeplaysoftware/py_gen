#
#    Copyright (C) Codeplay Software Limited. All Rights Reserved.
#
from py_gen.internal.funcs import (read_from_file, insert_in_source, write_to_file,
                           clang_format)
from py_gen.internal.iters import (dispatch_iterations, combined_dispatcher,
                           removal_dispatcher, combined_removal_dispatcher)
from py_gen.iter_classes import IterGroup, RemovalIterGroup


def generate_source(source, iter_groups):
    """Generates strings from the IterGroup and/or RemovalIterGroup objects in
    iter_groups, then inserts the generated strings into the input string,
    source.

    iter_groups is a list of IterGroup and/or RemovalIterGroup objects, each of
    which contains an insertion point, string Template and list of Iterable
    objects. The insertion point denotes the string in the source to be replaced
    by the result of substituting ${} keys in the string Template with the
    output of the Iterable object.

    More extensive explanation is contained within the internal documentation"""
    for iter_group in iter_groups:
        template = iter_group.template
        # Normal IterGroup
        if isinstance(iter_group, IterGroup):
            if iter_group.combine_iters:
                template = combined_dispatcher(template, iter_group.iterables)
            else:
                template = dispatch_iterations(template, iter_group.iterables)
        # Removal IterGroup
        else:
            if iter_group.combine_iters:
                template = combined_removal_dispatcher(
                    template, iter_group.insertion_iterables,
                    iter_group.removal_iterables)
            else:
                template = removal_dispatcher(template,
                                              iter_group.insertion_iterables,
                                              iter_group.removal_iterables)
        source = insert_in_source(source, iter_group.insertion_point,
                                  template.template)
    return source


def generate_file(input_file_name,
                  output_file_name,
                  iter_groups,
                  format_generated=False,
                  format_script=""):
    """Reads from file_name.in then generates and inserts strings into the read
    source, after which the result is written to file_name

    iter_groups is a list of IterGroup objects, each of which contains an
    insertion point, string Template and list of Iterable objects. The insertion
    point denotes the string in the source to be replaced by the result of
    substituting ${} keys in the string Template with the output of the Iterable
    object.

    More extensive explanation is contained within the internal documentation"""
    source = read_from_file(input_file_name)
    source = generate_source(source, iter_groups)
    write_to_file(output_file_name, source)
    if format_generated:
        clang_format(output_file_name, format_script)
    return source
