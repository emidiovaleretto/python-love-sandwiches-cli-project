from credentials import SHEET


def print_instructions():
    """
    Print the instructions to the terminal.
    """
    print("""
    Please enter sales data from last market day.
    Data should be six numbers, separated by commas.
    Example: 10, 20, 30, 40, 50, 60
    """)


def get_sales_data():
    """
    Returns sales figures imput from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be six integers separated by commas.
    The loop will continue to prompt the user until the data is valid.
    """
    while True:

        print_instructions()
        data_str = input('Enter your data here:\n')

        data_list = data_str.split(',')

        is_valid = validate_data(data_list)

        if is_valid:
            break

    return data_list


def validate_data(values):
    """
    Validates the data input from the user.
    Inside the try/except block, the user is prompted 
    to enter the correct data. Raises a ValueError if 
    there aren't exactly six values.
    """
    try:
        [int(values) for values in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values must be entered and you provided '
                f'{len(values)} value(s)')

    except ValueError as err:
        print(f'Invalid data: {err}, please try again.')
        return False

    return True


def calculate_surplus_data(sales_data):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figures subtracted from the stock figures.
    - Positive values indicate waste.
    - Negative values indicate extra made when stock was sold out.
    """
    print('Calculating surplus data...')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, surplus in zip(stock_row, sales_data):
        surplus = int(stock) - surplus
        surplus_data.append(surplus)

    return surplus_data


def calculate_stock_data(data):
    """
    Calculate the stock data from the sales data.
    """
    print('Calculating stock data...')

    stock_data = []

    for stock in data:
        int_stock = [int(num) for num in stock]
        average = sum(int_stock) / len(int_stock)
        new_stock = round(average * 1.1)
        stock_data.append(new_stock)

    return stock_data


def update_worksheet(data, worksheet_name):
    """
    Update the worksheet with the data provided.
    """
    print(f'Updating {worksheet_name} worksheet...')
    worksheet = SHEET.worksheet(f'{worksheet_name}')
    worksheet.append_row(data)
    print(f'{worksheet_name.capitalize()} worksheet updated successfully.')


def get_last_5_entires_sales():
    """
    Get the last 5 entries from the sales worksheet
    and returns the data as a list of lists.
    """
    worksheet = SHEET.worksheet('sales')

    columns = []
    for i in range(1, 7):
        column = worksheet.col_values(i)
        columns.append(column[-5:])

    return columns


def get_stock_values(data):
    """
    Gets the stock figures from the stock worksheet
    and return a string representation of the number
    of sandwiches to be made for next market day.
    """

    headings = SHEET.worksheet('stock').get_all_values()[0]

    print('Make the following number of sandwiches for next market:\n')

    dt_dict = dict(zip(headings, data))

    return dt_dict


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entires_sales()
    new_stock = calculate_stock_data(sales_columns)
    update_worksheet(new_stock, 'stock')
    get_stock_values(new_stock)
