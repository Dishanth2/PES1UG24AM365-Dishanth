def notes_needed(amount):
    """
    Calculate the number of 100 currency notes needed for a given withdrawal amount.
    
    Expected Format:
        String representing a non-negative integer amount, optionally containing commas
        as thousands separators (e.g., '2,500' or '2500').
        
    Returns:
        int: amount // 100 if input is valid.
        None: If input is invalid, non-string, malformed, negative, or contains decimals/symbols.
    """
    if not isinstance(amount, str):
        return None
    
    cleaned = amount.strip()
    if not cleaned:
        return None
    
    raw = cleaned.replace(',', '')
    if not raw:
        return None
    
    try:
        val = int(raw)
    except ValueError:
        return None
    
    if val < 0:
        return None
    
    return val // 100


def mask_card(card_number):
    """
    Mask a 16-digit card number in the format 'XXXX XXXX XXXX dddd'.
    
    Expected Format:
        String containing 4 space-separated groups of exactly 4 digits each
        (e.g., '1234 5678 9012 3456').
        
    Returns:
        str: 'XXXX XXXX XXXX ' + last_group if input is valid.
        None: If input is invalid, non-string, malformed, contains non-digits,
              or does not have exactly 4 four-digit groups.
    """
    if not isinstance(card_number, str):
        return None
    
    cleaned = card_number.strip()
    if not cleaned:
        return None
    
    groups = cleaned.split()
    if len(groups) != 4:
        return None
    
    for g in groups:
        if len(g) != 4 or not g.isdigit():
            return None
    
    return "XXXX XXXX XXXX " + groups[3]


def average_withdrawal(amounts_csv):
    """
    Calculate the integer floor average of withdrawal amounts provided as a CSV string.
    
    Expected Format:
        CSV string of non-negative integer withdrawal amounts (e.g., '500,1000,2000').
        
    Returns:
        int: sum(amounts) // len(amounts) if valid.
        None: If input is invalid, empty, malformed, contains empty tokens,
              non-integers, or negative amounts.
    """
    if not isinstance(amounts_csv, str):
        return None
    
    cleaned = amounts_csv.strip()
    if not cleaned:
        return None
    
    tokens = cleaned.split(',')
    if not tokens:
        return None
    
    values = []
    for token in tokens:
        t = token.strip()
        if not t:
            return None
        try:
            val = int(t)
        except ValueError:
            return None
        if val < 0:
            return None
        values.append(val)
    
    if not values:
        return None
    
    return sum(values) // len(values)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", result)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", result)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", result)


if __name__ == "__main__":
    main()
