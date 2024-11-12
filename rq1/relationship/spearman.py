import numpy as np
from scipy.stats import spearmanr, pearsonr

def calculate_spearman_coefficient(x, y):
    """
    Calculates the Spearman rank correlation coefficient between two arrays.
    
    Parameters:
    x (array-like): First array of values.
    y (array-like): Second array of values.
    
    Returns:
    tuple: Spearman rank correlation coefficient and p-value.
    """
    # Convert inputs to numpy arrays if they're not already
    x = np.array(x)
    y = np.array(y)
    
    # Check if the lengths of the arrays match
    if len(x) != len(y):
        raise ValueError("Arrays x and y must have the same length.")
    
    # Calculate Spearman rank correlation coefficient and p-value
    spearman_coefficient, p_value = spearmanr(x, y)
    
    return spearman_coefficient, p_value


def calculate_pearson_coefficient(x, y):
    """
    Calculates the Pearson correlation coefficient between two arrays using scipy.stats.
    
    Parameters:
    x (array-like): First array of values.
    y (array-like): Second array of values.
    
    Returns:
    tuple: Pearson correlation coefficient and p-value.
    """
    # Calculate Pearson correlation coefficient and p-value
    pearson_coefficient, p_value = pearsonr(x, y)
    
    return pearson_coefficient, p_value

x1 = [21, 15, 20, 16, 20, 21, 14] # No of years
x2 = [108, 37, 231, 14, 31, 316, 1388] # No of TDC
y = [869, 260, 3316, 151, 660, 2070, 17105] # No deleted tests

print("Duration Vs Deleted Tests")

spearman_coefficient, p_value = calculate_spearman_coefficient(x1, y)
print(f"Spearman Rank Correlation Coefficient: {spearman_coefficient}")
print(f"P-value: {p_value}")


# pearson_coefficient, p_value = calculate_pearson_coefficient(x1, y)
# print(f"Pearman Rank Correlation Coefficient: {pearson_coefficient}")
# print(f"P-value: {p_value}")


print("TDC VS Deleted Tests")

spearman_coefficient, p_value = calculate_spearman_coefficient(x2, y)
print(f"Spearman Rank Correlation Coefficient: {spearman_coefficient}")
print(f"P-value: {p_value}")


# pearson_coefficient, p_value = calculate_pearson_coefficient(x2, y)
# print(f"Pearman Rank Correlation Coefficient: {pearson_coefficient}")
# print(f"P-value: {p_value}")