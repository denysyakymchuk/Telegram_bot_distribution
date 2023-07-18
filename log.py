def write_logs(error):
    with open('logs.txt', 'a') as file:
        file.write(f'{str(error)}\n\n')
        file.flush()
