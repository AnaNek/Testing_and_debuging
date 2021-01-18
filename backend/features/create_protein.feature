Feature: Create protein

    Scenario Outline: Authenticated user can create protein
        Given An authenticated user 
        When I create protein with sequence <seq>
        Then I can see protein with sequence <seq> and status code <status>

        Examples:
            | seq    | status |
            | AAA    | 200    |
            | GCC    | 200    |
