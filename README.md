pyfpdf_hack
===========

web2py pyfpdf hack for &lt;, >, and &amp; in tables


The html to pdf routine inserts a new cell when it sees a lt, gt, amp, or apos.  
This causes incorrect PDF output that adds a column to the table when one of thes characters is encountered. 
For example, the following table in HTML 

--------------------------------------------------------------------
| row 1       | It's a boy     |  Wt > 4 kg     | len < 40cm       |
|-------------|----------------|----------------|------------------|
| row 2       | boy & girl     |  Wt > 3kg      | len < 35 cm      |
--------------------------------------------------------------------

is converted to the following PDF
--------------------------------------------------------------------
| row 1       | It             | s a boy        | Wt               |
|-------------|----------------|----------------|------------------|
| row 2       | boy            | girl           | Wt               |
--------------------------------------------------------------------

The hack is in modules/html.py.  It adds a string buffer and a switch.  The switch is turned on when the program is 
processing a table column \<TD\>.  
While the switch is on, the handle\_data() function's td handler will push the txt data into the 'cell\_txt' buffer. 
When the end of the column\</TD\> is reached the switch is turned off and handle_data() is called. 
In this way the entire string is placed into a single PDF cell.

SEE: controllers/default.py/listing() and modules/html.py
