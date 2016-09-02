from fpdf import FPDF
from datetime import date
import pprint

class PDF(FPDF):

    def header(self):

        # self.image('mario.png', 10, 8, 33)
        self.set_font('Arial', 'B', 14)
        pdf.cell(w=0, h=0, txt='{} - {}'.format(main_title, date.today().isoformat()), border=0, ln=0,  align='C', fill=False, link='')

    def footer(self):

        self.set_y(-15)
        self.set_font('Arial', 'I', 7)
        self.cell(0, 10, 'page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


main_title = 'Material Library'
pdf = PDF(orientation='P', unit='pt', format='A4')
pdf.set_creator(creator='johan@petfactory.se')
pdf.set_title(title=main_title)
pdf.alias_nb_pages()



total_width = 595
total_height = 842

grid_total_width = 580.0
grid_total_height = 790.0

grid_num_cols = 3
grid_num_rows = 4

grid_offset_x = (total_width - grid_total_width) *.5
grid_offset_y = 30

def build_placement_grid(total_width, total_height, grid_total_width, grid_total_height, grid_num_cols, grid_num_rows, grid_offset_x, grid_offset_y):

    
    grid_width = grid_total_width / float(grid_num_cols)
    grid_height = grid_total_height / float(grid_num_rows)

    row_list = []
    col_list = []

    for row_index in range(grid_num_rows):

        row_list.append((row_index * grid_height + grid_height*.5) + grid_offset_y)

    for col_index in range(grid_num_cols):
        col_list.append((col_index * grid_width + grid_width*.5) + grid_offset_x)


    return (tuple(row_list), tuple(col_list))


def buildPage(name_list, row_list, col_list, pdf):

    pdf.set_font('Times', '', 12)

    #pdf.rect(x=grid_offset_x, y=grid_offset_y, w=grid_total_width, h=grid_total_height, style = '')

    img_width = 160.0
    size = 10

    for index, name in enumerate(name_list):
        #print index, name
        row = index/(grid_num_rows-1)
        col = index%(grid_num_cols)

        print row, col
        x = col_list[col]
        y = row_list[row]

        pdf.image('mario_300_frame.png', x=x-img_width*.5, y=y-img_width*.5, w=img_width, h=img_width)

        pdf.rect(x=x-size*.5, y=y-size*.5, w=size, h=size, style = 'F')

        pdf.text(x=x-img_width*.5, y=y+14+img_width*.5, txt='{} {}'.format(index, name))


# Instantiation of inherited class
# 842 x 595

row_list, col_list = build_placement_grid(total_width, total_height, grid_total_width, grid_total_height, grid_num_cols, grid_num_rows, grid_offset_x, grid_offset_y)

seq = [c for c in 'abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQR']
chunk_length = 12
chunk_list = [seq[x:x+chunk_length] for x in xrange(0, len(seq), chunk_length)]

for chunk in chunk_list:

    pdf.add_page()
    buildPage(chunk, row_list, col_list, pdf)


pdf.output('mario.pdf', 'F')