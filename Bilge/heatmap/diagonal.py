import pandas as pd
from statistics import mean
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def get_cell_types(data, sep):
    '''
    Returns the unique cell types in a dataframe.
    
    Input:
        data: the dataframe where the columns are cell names
        sep: the separator that separates the cell type names
    
    Output:
        cells: a list of cell types
    '''
    cols = list(data.columns)
    cells = []
    for i in range(0, len(cols)):
        
        # Split the cell name based on separator and recombine the cell type
        cell_name = cols[i].split(sep)
        cell_type = sep.join(cell_name[2:])
        
        # Append the cell type to the list if it isn't already in it
        if cell_type not in cells:
            cells.append(cell_type)
    return cells

def rearrange_cell_types(data, cell_type_order, sep):
    '''
    Rearrange the cell types in a dataframe based on a specified order.
    
    Input:
        data: the dataframe where the columns are cell names
        cell_type_order: the order of cell types
    
    Output:
        order: the desired order of the cell names in the dataframe column
    '''
    
    # If the order is provided as a list of integers, convert it to a list of cell types
    if isinstance(cell_type_order[0], int):
        cell_types = get_cell_types(data, sep)
        for i in range(len(cell_type_order)):
            idx = cell_type_order[i]
            cell_type_order[i] = cell_types[idx]
    
    cols = list(data.columns)
    order = []
    
    # Loop through cell names and append according to the order
    for i in range(len(cell_type_order)):
        for j in range(len(cols)):
            if (cell_type_order[i] in cols[j] and cols[j] not in order):
                order.append(cols[j])
    return order

def get_mean_val(data, cell_type, row_name):
    '''
    Returns the mean value of a chromosome location based on cell type.
    
    Input:
        data: the dataframe where the columns are cell names
        cell_type: the cell type to analyze
        row_name: the chromosome location to analyze
        
    Output:
        the mean value of the chromosome location among the cell type
    '''
    
    vals = []
    
    # Append the value to the list if the cell type matches
    for name in list(df.columns):
        if cell_type in name:
            vals.append(float(df[name][row_name]))
    return mean(vals)

def get_col_vals(data, cell_type):
    '''
    Get the mean chromosome location values of all chromosome location based on cell type.
    
    Input:
        data: the dataframe where the columns are cell names
        cell_type: the desired cell type
        
    Output:
        cell_vals: a list of mean chromosome location values
        
    '''
    cell_vals = []
    for chr_pos in list(data.index):
        cell_vals.append((chr_pos, get_mean_val(df, cell_type, chr_pos)))
    return cell_vals

def find_correct_index(cell_vals, max_val):
    '''
    Based on the maximum value cutoff, get the first index to rearrange the chromosome locations.
    
    Input:
        cell_vals: a list of chromosome locations and mean values based on cell type
        max_val: maximum cutoff point for the blocks after they're sorted
        
    Output:
        the starting index to rearrange values'''
    values = list(zip(*cell_vals))[1]
    for i in range(0, len(values)):
        if values[i] > max_val:
            return i
    return -1

def diagonal(df, sep, max_val):
    '''Rearranges the indices of a dataframe so the DMR blocks are diagonal.
    
    Input: 
        df: the dataframe where the columns are cell names
        
    Output:
        idx_names: the list of the correct order of indices'''
    
    cell_types = get_cell_types(df, sep)
    idx_names = []
    idx = 0
    
    # Sort values for each cell_type based on the starting index
    for name in cell_types:
        cell_vals = get_col_vals(df, name)[idx:]
        cell_vals.sort(key = lambda x: x[1])
        idx_names[idx:] = list(zip(*cell_vals))[0]
        new_idx = find_correct_index(cell_vals, max_val)
        idx += new_idx
    
    return idx_names

if __name__ == '__main__':
    # The order of arguments
    # 1. file name
    # 2. max_val
    # 3. separator (i.e. '-')
    # 4. name of the heatmap file (pdf)
    # 5. name of the table (tsv)
    # 6+ order (given as separate integers based on which position each cell type should be in the heatmap)
    args = sys.argv
    file = args[1]
    max_val = float(args[2])
    sep = args[3]
    
    # Read the file
    data = pd.read_csv(file, sep='\t', index_col = 0)
    df = pd.DataFrame(data)
    
    # Rearrange the cell types if necessary
    if (len(args) > 6):
        order = []
        for i in range(6, len(args)):
            order.append(int(args[i]))
        new_order = rearrange_cell_types(df, order, sep)
        df = df[new_order]

    
    index_names = diagonal(df, sep, max_val)
    df = df.reindex(index_names)
    
    df.to_csv(args[5], sep = '\t')
    
    sns.heatmap(df)
    plt.savefig(args[4], bbox_inches='tight')