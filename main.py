import kivy
kivy.require('2.2.0')

_version_ = "1.2.3"   # for buildozer

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen



SYMBOLS_IN_LINE = 14

mem_str = '0'


class ScreenCalc1(Screen):
    
    txt_input_active = 1


    def but_change_field(self, instance):
        if   instance.text == '1':  
            self.txt_input_active = 1
            print(f'but_change_field pressed: {instance.text}')
        elif instance.text == '2':  
            self.txt_input_active = 2
            print(f'but_change_field pressed: {instance.text}')
        elif instance.text == '3':  self.txt_input_active = 3
        elif instance.text == '4':  self.txt_input_active = 4


    def but_pressed(self, instance):
        str_tmp = ''
        match self.txt_input_active:
            case 1: str_tmp = self.txt_lbl1.text
            case 2: str_tmp = self.txt_lbl2.text
            case 3: str_tmp = self.txt_lbl3.text
            case 4: str_tmp = self.txt_lbl4.text

        # performing all we need with string
        if len(str_tmp) == SYMBOLS_IN_LINE:  str_tmp = str_tmp + '\n'
        str_tmp = str_tmp + instance.text

        match self.txt_input_active:
            case 1: self.txt_lbl1.text = str_tmp
            case 2: self.txt_lbl2.text = str_tmp
            case 3: self.txt_lbl3.text = str_tmp
            case 4: self.txt_lbl4.text = str_tmp
        print(f'button text is {instance.text}')


    def but_pressed_func(self, instance):
        global mem_str
        str_tmp = ''
        match self.txt_input_active:
            case 1: str_tmp = self.txt_lbl1.text
            case 2: str_tmp = self.txt_lbl2.text
            case 3: str_tmp = self.txt_lbl3.text
            case 4: str_tmp = self.txt_lbl4.text
        match instance.text:
            case '=':
                translation_table = dict.fromkeys(map(ord, '\n'), None) # deleting
                str_tmp = str_tmp.translate(translation_table)          # '\n'
                str_tmp = str(eval(str_tmp))
                if len(str_tmp) > SYMBOLS_IN_LINE:  str_tmp = str_tmp[ :SYMBOLS_IN_LINE] + '\n' + str_tmp[SYMBOLS_IN_LINE: ]  # adding '\n' again
            case 'del':  str_tmp = str_tmp[:len(str_tmp) - 1]
            case 'clc':  str_tmp = ''
            case 'mr':  mem_str = str_tmp
            case 'ms':  str_tmp = str_tmp + mem_str
        match self.txt_input_active:
            case 1: self.txt_lbl1.text = str_tmp
            case 2: self.txt_lbl2.text = str_tmp
            case 3: self.txt_lbl3.text = str_tmp
            case 4: self.txt_lbl4.text = str_tmp





class ScreenCalc2(Screen):
    
    txt_input_active, operator1, operation, bin_expr_str = 'dec', '', '', ''


    def but_pressed(self, instance):
        str_tmp = ''
        num_tmp = 0
        match self.txt_input_active:
            case 'dec': str_tmp = self.calc2_txt1.text
            case 'hex': str_tmp = self.calc2_txt2.text
            case 'bin': str_tmp = self.bin_expr_str

        str_tmp = str_tmp + instance.text       # performing all we need with string

        match self.txt_input_active:
            case 'dec': num_tmp = int(str_tmp)
            case 'hex': num_tmp = int(str_tmp, 16)
            case 'bin': num_tmp = int(str_tmp, 2)

        self.calc2_txt1.text = str(num_tmp)
        self.calc2_txt2.text = hex(num_tmp)
        self.bin_expr_str = bin(num_tmp)
        str_tmp = self.bin_expr_str
        str_tmp = str_tmp if len(str_tmp) <= SYMBOLS_IN_LINE else str_tmp[:SYMBOLS_IN_LINE] + '\n' + str_tmp[SYMBOLS_IN_LINE:len(str_tmp)]
        self.calc2_txt3.text = str_tmp
        self.bin_write(bin(int(num_tmp)))


    def but_pressed_func(self, instance):

        global mem_str
        str_tmp, num_tmp = '', 0

        match self.txt_input_active:
            case 'dec': str_tmp = self.calc2_txt1.text
            case 'hex': str_tmp = self.calc2_txt2.text
            case 'bin': str_tmp = self.bin_expr_str

        match instance.text:
            case '=':
                print(self.operator1 + self.operation + str_tmp)
                num_tmp = eval(self.operator1 + self.operation + str_tmp)
                self.operator1 = ''                
            case 'del' | 'ms':
                if instance.text == 'del':  str_tmp = str_tmp[:len(str_tmp) - 1]
                if instance.text == 'ms':   str_tmp = mem_str
                match self.txt_input_active:
                    case 'dec': num_tmp = int(str_tmp)
                    case 'hex': num_tmp = int(str_tmp, 16)
                    case 'bin': num_tmp = int(str_tmp, 2)
                self.calc2_txt1.text = str(num_tmp)
                self.calc2_txt2.text = hex(num_tmp)
                self.bin_expr_str = bin(num_tmp)
                str_tmp = self.bin_expr_str
                str_tmp = str_tmp if len(str_tmp) <= SYMBOLS_IN_LINE else str_tmp[:SYMBOLS_IN_LINE] + '\n' + str_tmp[SYMBOLS_IN_LINE:len(str_tmp)]
                self.calc2_txt3.text = str_tmp
                str_tmp = bin(int(num_tmp))
                if len(str_tmp) < 34:   # fill 0's MSBits to four bytes in binary
                    for i in range(34 - len(str_tmp)):  str_tmp = str_tmp[:2] + '0' + str_tmp[2:len(str_tmp)]
                self.bin_write(str_tmp)
                return
            case 'clc':
                str_tmp = ''
                self.calc2_txt1.text = str_tmp
                self.calc2_txt2.text = str_tmp
                self.calc2_txt3.text = str_tmp
                self.bin_expr_str = str_tmp
                for i in range(34):  str_tmp = str_tmp + '0'
                self.bin_write(str_tmp)     # write alll 0's
                return
            case 'mr':  
                mem_str = str_tmp
                return
            #case 'ms':  str_tmp = str_tmp + mem_str
            case '+' | '-' | '*' | '/':
                if self.operator1 == '':  self.operation = instance.text
                self.operator1 = str_tmp
                self.calc2_txt1.text = self.calc2_txt2.text = self.calc2_txt3.text = self.bin_expr_str = ''
                return

        self.calc2_txt1.text = str(int(num_tmp))
        self.calc2_txt2.text = hex(int(num_tmp))
        self.bin_expr_str = bin(num_tmp)
        str_tmp = self.bin_expr_str
        str_tmp = str_tmp if len(str_tmp) <= SYMBOLS_IN_LINE else str_tmp[:SYMBOLS_IN_LINE] + '\n' + str_tmp[SYMBOLS_IN_LINE:len(str_tmp)]
        self.calc2_txt3.text = str_tmp
        self.bin_write(bin(int(num_tmp)))


    def but_pressed_bin(self, instance):

        id = instance.my_id
        num_tmp = 0

        str_tmp = self.bin_expr_str
        if str_tmp == '':  str_tmp = '0b0'          # in case when calc just started
        str_tmp_len = len(str_tmp)
        new_val_str = '0' if instance.text=='1' else '1'
        instance.text = new_val_str

        if id+3 > str_tmp_len:                      # fill 0-s MSBits if necessary
            for i in range((id+3) - str_tmp_len):
                str_tmp = str_tmp[ : 2] + '0' + str_tmp[2 : len(str_tmp)]
            str_tmp_len = len(str_tmp)

        str_tmp = str_tmp[ : str_tmp_len - (id+1)] + new_val_str + str_tmp[str_tmp_len - id : str_tmp_len]

        self.bin_expr_str = str_tmp
        num_tmp = int(str_tmp, 2)
        self.calc2_txt1.text = str(int(num_tmp))
        self.calc2_txt2.text = hex(int(num_tmp))
        str_tmp = str_tmp if len(str_tmp) <= SYMBOLS_IN_LINE else str_tmp[:SYMBOLS_IN_LINE] + '\n' + str_tmp[SYMBOLS_IN_LINE:len(str_tmp)]
        self.calc2_txt3.text = str_tmp


    def but_change_field(self, instance):
        self.txt_input_active = instance.text
        self.calc2_but_2.disabled = self.txt_input_active == 'bin'
        self.calc2_but_3.disabled = self.txt_input_active == 'bin'
        self.calc2_but_4.disabled = self.txt_input_active == 'bin'
        self.calc2_but_5.disabled = self.txt_input_active == 'bin'
        self.calc2_but_6.disabled = self.txt_input_active == 'bin'
        self.calc2_but_7.disabled = self.txt_input_active == 'bin'
        self.calc2_but_8.disabled = self.txt_input_active == 'bin'
        self.calc2_but_9.disabled = self.txt_input_active == 'bin'
        self.calc2_but_a.disabled = self.txt_input_active == 'dec' or self.txt_input_active == 'bin'
        self.calc2_but_b.disabled = self.txt_input_active == 'dec' or self.txt_input_active == 'bin'
        self.calc2_but_c.disabled = self.txt_input_active == 'dec' or self.txt_input_active == 'bin'
        self.calc2_but_d.disabled = self.txt_input_active == 'dec' or self.txt_input_active == 'bin'
        self.calc2_but_e.disabled = self.txt_input_active == 'dec' or self.txt_input_active == 'bin'
        self.calc2_but_f.disabled = self.txt_input_active == 'dec' or self.txt_input_active == 'bin'


    def bin_write(self, bin_str):
        bin_str_len = len(bin_str)
        self.calc2_bit0.text = bin_str[bin_str_len-1:bin_str_len]
        if bin_str_len >= 4: self.calc2_bit1.text = bin_str[bin_str_len-2:bin_str_len-1]
        if bin_str_len >= 5: self.calc2_bit2.text = bin_str[bin_str_len-3:bin_str_len-2]
        if bin_str_len >= 6: self.calc2_bit3.text = bin_str[bin_str_len-4:bin_str_len-3]
        if bin_str_len >= 7: self.calc2_bit4.text = bin_str[bin_str_len-5:bin_str_len-4]
        if bin_str_len >= 8: self.calc2_bit5.text = bin_str[bin_str_len-6:bin_str_len-5]
        if bin_str_len >= 9: self.calc2_bit6.text = bin_str[bin_str_len-7:bin_str_len-6]
        if bin_str_len >= 10: self.calc2_bit7.text = bin_str[bin_str_len-8:bin_str_len-7]
        if bin_str_len >= 11: self.calc2_bit8.text = bin_str[bin_str_len-9:bin_str_len-8]
        if bin_str_len >= 12: self.calc2_bit9.text = bin_str[bin_str_len-10:bin_str_len-9]
        if bin_str_len >= 13: self.calc2_bit10.text = bin_str[bin_str_len-11:bin_str_len-10]
        if bin_str_len >= 14: self.calc2_bit11.text = bin_str[bin_str_len-12:bin_str_len-11]
        if bin_str_len >= 15: self.calc2_bit12.text = bin_str[bin_str_len-13:bin_str_len-12]
        if bin_str_len >= 16: self.calc2_bit13.text = bin_str[bin_str_len-14:bin_str_len-13]
        if bin_str_len >= 17: self.calc2_bit14.text = bin_str[bin_str_len-15:bin_str_len-14]
        if bin_str_len >= 18: self.calc2_bit15.text = bin_str[bin_str_len-16:bin_str_len-15]
        if bin_str_len >= 19: self.calc2_bit16.text = bin_str[bin_str_len-17:bin_str_len-16]
        if bin_str_len >= 20: self.calc2_bit17.text = bin_str[bin_str_len-18:bin_str_len-17]
        if bin_str_len >= 21: self.calc2_bit18.text = bin_str[bin_str_len-19:bin_str_len-18]
        if bin_str_len >= 22: self.calc2_bit19.text = bin_str[bin_str_len-20:bin_str_len-19]
        if bin_str_len >= 23: self.calc2_bit20.text = bin_str[bin_str_len-21:bin_str_len-20]
        if bin_str_len >= 24: self.calc2_bit21.text = bin_str[bin_str_len-22:bin_str_len-21]
        if bin_str_len >= 25: self.calc2_bit22.text = bin_str[bin_str_len-23:bin_str_len-22]
        if bin_str_len >= 26: self.calc2_bit23.text = bin_str[bin_str_len-24:bin_str_len-23]
        if bin_str_len >= 27: self.calc2_bit24.text = bin_str[bin_str_len-25:bin_str_len-24]
        if bin_str_len >= 28: self.calc2_bit25.text = bin_str[bin_str_len-26:bin_str_len-25]
        if bin_str_len >= 29: self.calc2_bit26.text = bin_str[bin_str_len-27:bin_str_len-26]
        if bin_str_len >= 30: self.calc2_bit27.text = bin_str[bin_str_len-28:bin_str_len-27]
        if bin_str_len >= 31: self.calc2_bit28.text = bin_str[bin_str_len-29:bin_str_len-28]
        if bin_str_len >= 32: self.calc2_bit29.text = bin_str[bin_str_len-30:bin_str_len-29]
        if bin_str_len >= 33: self.calc2_bit30.text = bin_str[bin_str_len-31:bin_str_len-30]
        if bin_str_len >= 34: self.calc2_bit31.text = bin_str[bin_str_len-32:bin_str_len-31]





class ScreenCalc2bin(Screen):
    
    def on_pre_enter(self):
        pass




class SettingsScreen(Screen):
    pass





class Mycalc2App(App):

    def build(self):
        # Create the screen manager
        #sm = ScreenManager(transition='in_back')
        sm = ScreenManager()
        sm.add_widget(ScreenCalc2(name='calc2'))
        sm.add_widget(ScreenCalc2bin(name='calc2bin'))
        sm.add_widget(ScreenCalc1(name='calc1'))
        sm.add_widget(SettingsScreen(name='menu'))

        return sm


if __name__ == '__main__':
    Mycalc2App().run()
