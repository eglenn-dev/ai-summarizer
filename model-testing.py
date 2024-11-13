import math

def calculate_summary_length(document_length, max_summary_length, k, m):
    return max_summary_length / (1 + math.exp(-k * (document_length - m)))

# Example usage
document_length = 500  # Length of the document in words
max_summary_length = 300  # Maximum desired summary length in words
k = 0.001  # Steepness parameter
m = 2500  # Midpoint parameter

summary_length = calculate_summary_length(document_length, max_summary_length, k, m)
print("Desired summary length:", summary_length)

def calculate_bullet_points(document_length, max_summary_length, k=0.001, m=2500):
    return math.ceil((max_summary_length / (1 + math.exp(-k * (document_length - m)))) / 20)