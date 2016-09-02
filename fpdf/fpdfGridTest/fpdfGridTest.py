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
        #self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 7)
        # Page number
        self.cell(0, 10, 'page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


main_title = 'Material Library'
pdf = PDF(orientation='P', unit='pt', format='A4')
pdf.set_creator(creator='johan@petfactory.se')
pdf.set_title(title=main_title)
pdf.alias_nb_pages()




# Instantiation of inherited class
# 842 x 595


total_width = 595
total_height = 842

grid_total_width = 580.0
grid_total_height = 790.0

num_grid_x = 3
num_grid_y = 4


grid_offset_x = (total_width - grid_total_width) *.5
grid_offset_y = 30

grid_width = grid_total_width / float(num_grid_x)
grid_height = grid_total_height / float(num_grid_y)

col_list = []
for col in range(num_grid_x):
    col_list.append((col * grid_width + grid_width*.5) + grid_offset_x)

row_list = []
for row in range(num_grid_y):
    row_list.append((row * grid_height + grid_height*.5) + grid_offset_y)


def buildPage(pdf):


    pdf.add_page()
    pdf.set_font('Times', '', 12)

    #pdf.rect(x=grid_offset_x, y=grid_offset_y, w=grid_total_width, h=grid_total_height, style = '')

    img_width = 160.0
    size = 10

    index = 0
    for row in row_list:

        for col in col_list:
            #print row, col
            index += 1

            pdf.image('mario_300_frame.png', x=col-img_width*.5, y=row-img_width*.5, w=img_width, h=img_width)

            pdf.rect(x=col-size*.5, y=row-size*.5, w=size, h=size, style = 'F')

            pdf.text(x=col-img_width*.5, y=row+14+img_width*.5, txt='{} Material name'.format(index))



for mat in range(40):
    if mat % (num_grid_x*num_grid_y) == 0:
        print 'new'
        buildPage(pdf)



pdf.output('mario.pdf', 'F')