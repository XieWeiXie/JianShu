import copy
def json_to_mysql(json_obj, table, sql_type="insert"):
    local_copy = copy.deepcopy(json_obj)
    if sql_type == "insert":
        sql_part1 = "insert into " + table
        keys = local_copy.keys()

        sql_part2 = "("
        for key in keys:
            sql_part2 += "`%s`"%(key)
            sql_part2 += ","
        sql_part2 = sql_part2.rstrip(",")
        sql_part2 += ")"

        sql_part3 = "("
        for key in keys:
            sql_part3 += "'" + (local_copy[key]) + "'"
            sql_part3 += ","
        sql_part3 = sql_part3.rstrip(",")
        sql_part3 += ")"

        sql = sql_part1 + " " + sql_part2 + " values " + sql_part3

    elif sql_type == "select":
        del local_copy["id"]
        del local_copy["fetchtime"]
        del local_copy["crawler"]
        sql_part1 = "select count(*) from " + table + " where"
        keys = local_copy.keys()

        sql_part2 = "("
        for key in keys:
            sql_part2 += key
            sql_part2 += ","
        sql_part2 = sql_part2.rstrip(",")
        sql_part2 += ")"

        sql_part3 = "("
        for key in keys:
            sql_part3 += "'" + (local_copy[key]) + "'"
            sql_part3 += ","
        sql_part3 = sql_part3.rstrip(",")
        sql_part3 += ")"

        sql = sql_part1 + " " + sql_part2 + " = " + sql_part3

    return sql