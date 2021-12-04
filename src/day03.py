### Day 3, part 2

import argparse
import pandas as pd


def create_parser():
    """Parse command line values"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("input", help="input file")
    parser.add_argument(
        "--length",
        help="number of characters in the string",
        default="5",
    )
    return parser


# file = open("../data/day03_test.txt", "r")
# string_length = 5  # 5 for test data; 12 for input data

if __name__ == "__main__":
    args = create_parser().parse_args()
    arguments = vars(args)
    print(arguments)

    file = open(args.input, "r")
    string_length = int(args.length)  # 5 for test data; 12 for input data
    data = file.readlines()
    file.close()

    df = pd.DataFrame(columns=(range(string_length)))
    for i, line in enumerate(data):
        clean_line = line.rstrip("\n")
        df.loc[i] = [char for char in clean_line]

    def find_rating(df, tie_breaker, mask, count, method):
        if len(df[mask].index) == 1:
            rating = ""
            for j in range(string_length):
                rating += df[mask][j].values[0]
            print(
                f"converged at round {count}, on {rating} or decimal {int(rating, 2)}"
            )
            return int(rating, 2)
        else:
            criteria = df[mask][count].mode()
            # print(f"criteria info {df[mask][count].mode()}")
            if method == "max":
                criteria = (
                    tie_breaker if (len(criteria) > 1) else df[mask][count].mode()[0]
                )
                # print(f"df[mask][count].mode()[0] (max) = {df[mask][count].mode()[0]}")
                # print(f"criteria (max) = {criteria}")
            else:
                criteria = (
                    tie_breaker
                    if (len(criteria) > 1)
                    else df[mask][count].value_counts().idxmin()
                )
                # print(
                #     f"df[mask][count].value_counts().idxmin() (min) = {df[mask][count].value_counts().idxmin()}"
                # )
                # print(f"criteria (min) = {criteria}")
            addnl_mask = df[mask][count] == criteria
            new_mask = addnl_mask if all(mask) else (mask & addnl_mask)
            # print(f"matrix to assess column {count + 1}, chosen by {criteria}")
            # print(df[new_mask])
            return find_rating(df, tie_breaker, new_mask, count + 1, method)

    mask = [True] * len(df.index)
    # print("*****GET o_rate:")
    o_rate = find_rating(df, "1", mask, 0, "max")
    # print("*****GET c_rate:")
    c_rate = find_rating(df, "0", mask, 0, "min")
    life_support_rating = o_rate * c_rate
    print(f"life_support_rating = {life_support_rating}")
