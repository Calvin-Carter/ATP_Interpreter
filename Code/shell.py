import bogger

def main():
    while True:
        text = input ('bogger > ')
        result, error = bogger.run(text)

        if error: print(error, ':', text)
        else:
            print(result)

if __name__ == '__main__':
    main()