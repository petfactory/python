from fpdf import FPDF
from datetime import date

class PDF(FPDF):
    def header(self):
        # Logo
        # self.image('mario.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 14)
        # Move to the right
        #self.cell(80)
        # Title
        #self.cell(0, 10, , 0, 0, 'C')
        pdf.cell(w=0, h=0, txt='{} - {}'.format(main_title, date.today().isoformat()), border=0, ln=0,  align='C', fill=False, link='')
        # Line break
        self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


main_title = 'Material Library'
pdf = PDF(orientation='P', unit='pt', format='A4')
pdf.set_creator(creator='johan@petfactory.se')
pdf.set_title(title=main_title)
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 12)




total_width = 595
total_height = 842


grid_total_width = 400.0
grid_total_height = 400.0

num_grid_x = 4
num_grid_y = 4


grid_offset_x = 10
grid_offset_y = 10

grid_width = grid_total_width / float(num_grid_x)
grid_height = grid_total_height / float(num_grid_y)

col_list = []
for col in range(num_grid_x):
    col_list.append((col * grid_width + grid_width*.5) + grid_offset_x)

row_list = []
for row in range(num_grid_y):
    row_list.append((row * grid_height + grid_height*.5) + grid_offset_y)


pdf.rect(x=grid_offset_x, y=grid_offset_y, w=grid_total_width, h=grid_total_height, style = '')

img_width = 95.0
size = 10
for row in row_list:

    for col in col_list:
        #print row, col
        x = col-size*.5
        y = row-size*.5
        pdf.image('mario_300_frame.png', x=x-img_width*.5, y=y-img_width*.5, w=img_width, h=img_width)

        pdf.rect(x=x-size*.5, y=y-size*.5, w=size, h=size, style = 'F')



# Instantiation of inherited class
# 842 x 595
'''
total_width = 595
total_height = 842
num_grid_x = 3
edge_offset_x = 20
content_edge_offset_x = 30

num_grid_y = 4
edge_offset_y = 50
content_edge_offset_y = 15

grid_width_float = (total_width - edge_offset_x*2.0) / num_grid_x
grid_height_float = (total_height - edge_offset_y*2.0) / num_grid_y


#print grid_width_float
#print grid_height_float

for row in range(num_grid_y):

    for col in range(num_grid_x):

        x = col * grid_width_float + edge_offset_x
        y = row * grid_width_float + edge_offset_y

        img_x = x + content_edge_offset_x
        img_y = y + content_edge_offset_y
        img_width = grid_width_float-content_edge_offset_x*2

        pdf.rect(x=x, y=y, w=grid_width_float, h=grid_width_float, style = '')

        #fpdf.image(name, x = None, y = None, w = 0, h = 0, type = '', link = '')
        pdf.image('mario.png', x=img_x, y=img_y, w=img_width, h=img_width)

        pdf.rect(x=img_x, y=img_y, w=img_width, h=img_width, style = '')


'''

'''
x_inc = 50
y_inc = 50
inc = 0
for i in range(1, 5):

    pdf.rect(x=pdf.get_x(), y=pdf.get_y(), w=40, h=40, style='')
    pdf.text(x=pdf.get_x(), y=pdf.get_y(), txt='{}'.format(i))
    pdf.set_y(pdf.get_y() + y_inc)
    inc += 1

    if inc > 5:
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        inc = 0
 '''

pdf.output('tuto2.pdf', 'F')