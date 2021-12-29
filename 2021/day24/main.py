# Solved in a spreadsheet :)

# Notice that program is running 14 bloacks of almost identical code
# Each step is either blowing z out by 26, or it's possibly brining z in by 26 if the right inputs are given such that we get 0 in mod 26
# The only way to bring z down to solved is to meet the mod test every step it can
# Becasue of the *26 and mod 26 each step we can consider input valaidation to be happening in a push pop stack
# so for each chance to sovle the mod equality, need to look back to the last unused input

# therefore all pairs of inputs can be determined as needing to be a fixed range apart from one another
# then to pick the biggest and smalest numbers we just need to find the biggest and smallest solutions to each of those range equalities