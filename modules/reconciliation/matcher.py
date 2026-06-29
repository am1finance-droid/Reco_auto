import pandas as pd


class Matcher:

    def amount_match(
            self,
            books_df,
            statement_df
    ):

        books = books_df.copy()
        statement = statement_df.copy()

        books["amount"] = pd.to_numeric(
            books["amount"],
            errors="coerce"
        )

        statement["amount"] = pd.to_numeric(
            statement["amount"],
            errors="coerce"
        )

        matched = books.merge(
            statement,
            on="amount",
            how="inner",
            suffixes=(
                "_books",
                "_statement"
            )
        )

        matched["match_type"] = "Amount"

        matched["match_status"] = "Matched"

        return matched