def get_prep_indicators(values, prep_id) -> tuple:  # table info parser
    # getting average info
    average_nps = values[0][2]
    average_retirement = values[0][3]

    nps = 0
    retirement = 0
    redflags = 0

    # getting prep info
    for prep_info in values:
        if prep_info[1].isdigit() and int(prep_info[1]) == prep_id:
            if len(prep_info) >= 3:  # if nps and no retirement and no redflags
                nps = prep_info[2]
            if len(prep_info) >= 4:  # if nps and retirement and no redflags
                retirement = prep_info[3]
            if len(prep_info) >= 5:  # if nps and retirement and redflags
                redflags = prep_info[4]
    return nps, retirement, average_nps, average_retirement, redflags
