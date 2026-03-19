# This script is designed to encode numerical values with RGB codes
import numpy as np



def assign_color(values,
                 min_color, max_color,
                 min_value=None, max_value=None):
    
    """ Assigns RGB colors to a collection of values, on a 2-color gradient.

    Assigns RGB colors to a collection of values (values), given the
    pre-assigned colors for the minimum (min_color) and maximum (max_color)
    values. The manually assigned colors must be in RGB format
    (e.g. [255, 0, 255]).

    Parameters
    ----------
    values : list
        Numerical values to be RGB encoded.
    min_color : list
        RGB color code to be assigned to the lowest value
    max_color : list
        RGB color code to be assigned to the lowest value
    
    Returns
    -------
    list
        Assigned RGB color codes. Color code order matches "values" order.
    """
    
    # Automatically assign  minimum and maximum values if not explicitly stated
    values = list(values)
    if min_value == None:
        min_value = min(values)
    if max_value == None:
        max_value = max(values)
    
    # Scale values so min_value == 0 and max_value == 1
    val_range = max_value - min_value
    scaled_values = [(value - min_value) / val_range for value in values]
    
    # Obtain the difference of max and min RGB values
    min_color = np.array(min_color)
    max_color = np.array(max_color)
    color_diff = max_color - min_color
    
    # Assign RGB values based on scaled values
    rgb_values = [min_color + color_diff * i for i in scaled_values]
    rgb_values = [np.round(i) for i in rgb_values]
    rgb_values = [i.astype('i') for i in rgb_values]
    
    return rgb_values



def assign_ncolor(values, breaks, break_colors, return_dict=False):
    
    """ Assigns RGB colors to a collection of values, on an n-color gradient.

    Assigns RGB colors to a collection of values (values), given RGB colors
    (break_colors) that are pre-assigned to given values (breaks). This function
    builds off of assign_color, but can be used for an n-color gradient, rather
    than a 2 color gradient.
    
    Parameters
    ----------
    values : list
        Numerical values to be RGB encoded.
    breaks : list
        Numerical values that are to correspond to a given colour.
    break_colors : nested list
        Colours that are to correspond to a given value.
    return_dict : bool, optional
        Boolean if returned data should be in dictionary format (True) or a
        nested list (False).

    Returns
    -------
    nested list or dict
        Numerical values and their assigned RGB color code.
    """

    if len(breaks) != len(break_colors):
        return(
            f'Error: Number of given breaks ({len(breaks)}) does not'
            f'match number of given colors ({len(break_colors)})'
            )
    
    elif any([breaks[i] > breaks[i + 1] for i in range(0, len(breaks) - 1)]):
        return(
            f'Error: Ensure that breaks are sorted in ascending'
            f'value and that desired break colors match'
            )
    
    elif min(breaks) > min(values):
        return(f'Error: Minimum break larger than minimum value')
    
    elif max(breaks) < max(values):
        return(
            f'Error: Maximum break ({max(breaks)}) smaller'
            f'than maximum value ({max(values)})'
            )

    else:

        chunks = []

        for i in range(0, len(breaks) - 1):
            
            min_val = breaks[i]
            max_val = breaks[i + 1]

            min_col = break_colors[i]
            max_col = break_colors[i + 1]
            
            if i == (len(breaks) - 2):
                val_chunk = [
                    j for j in values if
                    (j >= min_val) & (j <= max_val)
                    ]
            else:
                val_chunk = [
                    j for j in values if
                    (j >= min_val) & (j < max_val)
                    ]
            
            rgb_chunk = assign_color(
                values=val_chunk,
                min_color=min_col,
                max_color=max_col,
                min_value=min_val,
                max_value=max_val
            )
            chunk = zip(val_chunk, rgb_chunk)
            chunk = [[i, j] for i, j in chunk]
            chunks.append(chunk)
        
        data = [i for j in chunks for i in j]

        if return_dict == True:
            data = dict(data)

        return data



if __name__ == "__main__":

    print('' \
    'Example usage of assign_ncolor with a seven' \
    'color gradient and 40 random values'
    )

    seq = np.random.randint(120, size=(50))

    x = [0, 20, 40, 60, 80, 100, 120]
    y = [
        [255,0,0], # Red
        [255,127,0], # Orange
        [255,255,0], # Yellow
        [0,255,0], # Green
        [0,0,255], # Blue
        [75,0,130], # Indigo
        [238, 130, 238] # Violet
        ]

    rgb_data = assign_ncolor(seq, x, y)

    rgb_data = np.array(rgb_data, dtype=object)
    rgb_data = np.array(
        sorted(rgb_data, key=lambda x: x[0]),
        dtype=object
        )

    for i, j in zip(x, y):

        r = j[0]
        g = j[1]
        b = j[2]
        text = f'Value: {i} | Assigned Color: {j}'
        print(f'\033[38;2;{r};{g};{b}m{text}\033[0m')
    
    print('\nEncoded Values')
    for i in range(0, rgb_data.shape[0]):
        val = rgb_data[i][0]
        col = rgb_data[i][1]
        r = col[0]
        g = col[1]
        b = col[2]
        text = f'Value: {val} | Encoded Color: {col}'
        print(f'\033[38;2;{r};{g};{b}m{text}\033[0m')
