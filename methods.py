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
        data_str = input('Enter your data here: ')

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


def update_sales_worksheet(values):
    """
    Updates the values in the worksheet,
    add a new row with the list data provided.
    """
    print('Updating sales worksheet...')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(values)
    print('Sales worksheet updated successfully.')


def calculate_surplus_data(sales_data):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figures subtracted from the stock figures.
    - Positive values indicate waste.
    - Negative values indicate extra made when stock was sold out.
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, surplus in zip(stock_row, sales_data):
        surplus = int(stock) - surplus
        surplus_data.append(surplus)

    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
