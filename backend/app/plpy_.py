""" Module for PlPython functions. """
# This module is named 'plpy_'
# to differentiate it from PlPython's built in 'plpy' module
from . import plpy_man
from sqlalchemy import event, DDL

from app.models import User, Answer, Question


_to_identifier_func = DDL(
    """\
CREATE FUNCTION _to_identifier_func() RETURNS TRIGGER AS $$
    import unicodedata
    disp_name = TD["new"]["display_name"]
    id_name = unicodedata.normalize("NFKD", disp_name).lower()
    TD["new"]["identifier_name"] = id_name
    if id_name.__contains__("admin"):
        count_row = plpy.execute("SELECT count(display_name) FROM public.user WHERE display_name='admin';")
        if count_row[0]['count'] > 0:
            raise ValueError("Name cannot be admin.")
        TD["new"]["number"] = 0
    if id_name.__contains__("#"):
        raise ValueError("The normalized name cannot contain the hash symbol")
    if len(id_name) > 32:
        raise ValueError("The normalized name cannot be longer than 32 characters")
    return "MODIFY"
$$ LANGUAGE PLPYTHON3U;"""
)
_to_identifier_trigger = DDL(
    """\
CREATE TRIGGER _to_identifier_trigger BEFORE INSERT OR UPDATE on public.user
FOR EACH ROW EXECUTE PROCEDURE _to_identifier_func();"""
)



def set_event_listeners():
    event.listen(
        User.__table__,
        "after_create",
        _to_identifier_func.execute_if(dialect="postgresql"),
    )

    event.listen(
        User.__table__,
        "after_create",
        _to_identifier_trigger.execute_if(dialect="postgresql"),
    )


















# _initialize_GD = DDL(
#     """\
# CREATE FUNCTION _initialize_GD() RETURNS INT AS $$
#     import functools
#
#
#     def _delete_element_that_references_previous_element(element, id_):
#         '''
#         Changes the previous element of the next element
#         if the current element is deleted.
#
#         Example:
#           Element table:
#             id | previous_answer
#             ---|---
#             1  | null
#             2  | 1
#             3  | 2
#
#           If element with id 2 is deleted,
#           this function changes element 3 so the table looks like this:
#             id | previous_answer
#             ---|---
#             1  | null
#             3  | 1
#         '''
#         # Todo: Optimize
#         select_plan = plpy.prepare(
#             f"SELECT previous_{element} FROM answer WHERE id = $1", ["UUID"]
#         )
#         rows = plpy.execute(select_plan, [id_])
#         if len(rows) > 1:
#             raise plpy.Error(
#             f"Tusky failed a sanity check: "
#             f"multiple elements have {id} listed as the previous element.",
#         )
#         previous_id = rows[0][f"previous_{element}"]
#         update_plan = plpy.prepare(
#             f"UPDATE answer SET previous_{element} = $1 WHERE previous_{element} = $2;",
#             ["UUID", "UUID"]
#         )
#         plpy.execute(
#             update_plan,
#             [previous_id, id_]
#         )
#         delete_plan = plpy.prepare(f"DELETE FROM {element} WHERE id = $1", ["UUID"])
#         plpy.execute(
#             delete_plan,
#             [id_]
#         )
#         return 1
#
#
#     delete_single_question = functools.partial(
#         _delete_element_that_references_previous_element,
#         "question"
#     )
#     delete_single_answer = functools.partial(
#         _delete_element_that_references_previous_element,
#         "answer"
#     )
#     GD["delete_single_question"] = delete_single_question
#     GD["delete_single_answer"] = delete_single_answer
#     plpy.log("Ran PlPython Global Dict initialization")
#     plpy.log("Global Dict contents:", GD)
#     return 0
# $$ LANGUAGE PLPYTHON3U;"""
# )
# event.listen(
#     User.__table__,
#     "after_create",
#     _initialize_GD.execute_if(
#         dialect="postgresql"
#     ),
# )
# _delete_single_answer = DDL(
#     """\
# CREATE FUNCTION delete_single_answer(answer_id UUID) RETURNS INT AS $$
#     plpy.log(GD)
#     print(GD)
#     return GD["delete_single_answer"](id_=answer_id)
# $$ LANGUAGE PLPYTHON3U;"""
# )
# event.listen(
#     Answer.__table__,
#     "after_create",
#     _delete_single_answer.execute_if(dialect="postgresql"),
# )
# _delete_single_question = DDL(
#     """\
# CREATE FUNCTION delete_single_question(question_id UUID) RETURNS INT AS $$
#     return GD["delete_single_question"](id_=question_id)
# $$ LANGUAGE PLPYTHON3U;"""
# )
# event.listen(
#     Question.__table__,
#     "after_create",
#     _delete_single_question.execute_if(dialect="postgresql"),
# )


# _to_identifier_func = DDL(
#     """\
# CREATE FUNCTION _to_identifier_func() RETURNS TRIGGER AS $$
#     import unicodedata
#     disp_name = TD["new"]["display_name"]
#     id_name = unicodedata.normalize("NFKD", disp_name).lower()
#     TD["new"]["identifier_name"] = id_name
#     if id_name.__contains__("admin"):
#         count_row = plpy.execute("SELECT count(display_name) FROM public.user WHERE display_name='admin';")
#         if count_row[0]['count'] > 0:
#             raise ValueError("Name cannot be admin.")
#         TD["new"]["number"] = 0
#     if id_name.__contains__("#"):
#         raise ValueError("The normalized name cannot contain the hash symbol")
#     if len(id_name) > 32:
#         raise ValueError("The normalized name cannot be longer than 32 characters")
#     return "MODIFY"
# $$ LANGUAGE PLPYTHON3U;"""
# )
# _to_identifier_trigger = DDL(
#     """\
# CREATE TRIGGER _to_identifier_trigger BEFORE INSERT OR UPDATE on public.user
# FOR EACH ROW EXECUTE PROCEDURE _to_identifier_func();"""
# )

# _delete_single_answer = DDL(
#     """\
# CREATE FUNCTION _delete_single_answer(id_ UUID) RETURNS INT AS $$
#     select_plan = plpy.prepare(
#         "SELECT previous_answer FROM answer WHERE id = $1", ["UUID"]
#     )
#     rows = plpy.execute(select_plan, [id_])
#     if len(rows) > 1:
#         raise plpy.Error(
#         f"Tusky failed a sanity check: "
#         f"multiple elements have {id} listed as the previous element.",
#     )
#     previous_id = rows[0]["previous_answer"]
#     update_plan = plpy.prepare(
#         "UPDATE answer SET previous_answer = $1 WHERE previous_answer = $2;",
#         ["UUID", "UUID"]
#     )
#     plpy.execute(
#         update_plan,
#         [previous_id, id_]
#     )
#     delete_plan = plpy.prepare(f"DELETE FROM answer WHERE id = $1", ["UUID"])
#     plpy.execute(
#         delete_plan,
#         [id_]
#     )
#     return 1
# $$ LANGUAGE PLPYTHON3U;"""
# )
#
# _delete_single_question = DDL(
#     """\
# CREATE FUNCTION _delete_single_question(id_ UUID) RETURNS INT AS $$
#     select_plan = plpy.prepare(
#         "SELECT previous_question FROM question WHERE id = $1", ["UUID"]
#     )
#     rows = plpy.execute(select_plan, [id_])
#     if len(rows) > 1:
#         raise plpy.Error(
#         f"Tusky failed a sanity check: "
#         f"multiple elements have {id} listed as the previous element.",
#     )
#     previous_id = rows[0]["previous_question"]
#     update_plan = plpy.prepare(
#         "UPDATE question SET previous_question = $1 WHERE previous_question = $2;",
#         ["UUID", "UUID"]
#     )
#     plpy.execute(
#         update_plan,
#         [previous_id, id_]
#     )
#     delete_plan = plpy.prepare(f"DELETE FROM question WHERE id = $1", ["UUID"])
#     plpy.execute(
#         delete_plan,
#         [id_]
#     )
#     return 1
# $$ LANGUAGE PLPYTHON3U;"""
# )


# def set_event_listeners():
#     event.listen(
#         User.__table__,
#         "after_create",
#         _to_identifier_func.execute_if(dialect="postgresql"),
#     )
#
#     event.listen(
#         User.__table__,
#         "after_create",
#         _to_identifier_trigger.execute_if(dialect="postgresql"),
#     )

    # event.listen(
    #     Answer.__table__,
    #     "after_create",
    #     _delete_single_answer.execute_if(dialect="postgresql"),
    # )
    #
    # event.listen(
    #     Question.__table__,
    #     "after_create",
    #     _delete_single_question.execute_if(dialect="postgresql"),
    # )
