def ref_data(data):
    records = []
    for item in data:
        record = f"{item[0]} - {item[1]}"
        records.append(record)

    result = ",\n".join(records)
    return result

