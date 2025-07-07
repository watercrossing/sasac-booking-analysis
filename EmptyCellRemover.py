from nbconvert.preprocessors import Preprocessor

class EmptyCellRemover(Preprocessor):
    """
    Remove cells that would be empty after input removal and output filtering
    """
    
    def preprocess(self, nb, resources):
        """
        Remove empty cells from the notebook
        """
        new_cells = []
        
        for cell in nb.cells:
            keep_cell = True
            
            if cell.cell_type == 'code':
                # Check if cell has outputs that won't be hidden
                has_visible_output = False
                
                if hasattr(cell, 'outputs') and cell.outputs:
                    # Check if this cell is tagged to hide outputs
                    cell_tags = cell.get('metadata', {}).get('tags', [])
                    if 'hide_output' not in cell_tags:
                        has_visible_output = True
                
                # Since we're hiding inputs, only keep if there's visible output
                if not has_visible_output:
                    keep_cell = False
            
            elif cell.cell_type == 'markdown':
                # Keep markdown cells if they have content
                if not cell.source.strip():
                    keep_cell = False
            
            if keep_cell:
                new_cells.append(cell)
        
        nb.cells = new_cells
        return nb, resources

# jupyter nbconvert --to html --no-input --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_all_outputs_tags hide_output --HTMLExporter.preprocessors EmptyCellRemover.EmptyCellRemover --TagRemovePreprocessor.remove_input_tags hide_input .\analysis.ipynb