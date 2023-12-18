


label_list = []
pre_list = []
delete_key = set()
key_label = {}
key_pre = {}
key_click_num = {}
key_impress_num = {}
sctr_map = {}
sku_imp = {}
sku_clk = {}
sku_sctr_imp = {}
sku_sctr_clk = {}
total_impress_num = 0
total_click = 0
sctr_imp = 0.0
sctr_clk = 0.0
sctr_ratio = 0.0




def cal_sctr_value(result_file_path):
    global total_impress_num
    global total_click
    global gauc
    global impress_gauc
    global chuangyi_sku_list
    global sctr_map
    f=open(result_file_path)
    all_lines=f.readlines()
    
    # get all predict labels

    for oneline in all_lines:
        elements=oneline.strip('\n').split('\t')
        # get click label, 1 for click samples, 0 for not clicked samples
        label = elements[1]
        # get peri-CR model predict result
        pre = elements[0]
        # get sku_id
        sku = elements[3]
        # get request id 
        sid = elements[2]
        # get creative expo lable in this request, 1 for exposed creative sampleds, 0 for unexposed creative sampleds
        expo = elements[4]

    # cal nsctr
        sctr_key = sid+'@'+sku
        sctr_value = [float(pre),float(expo),float(label)]
        if sctr_key in sctr_map:
            if sctr_map[sctr_key][0] < float(pre):
                sctr_map[sctr_key] = sctr_value
        else:
            sctr_map[sctr_key] = sctr_value
        if float(expo) != 1:
            continue
        if float(expo) == 1:
            if sku in sku_imp:
                sku_imp[sku] += 1
                sku_clk[sku] += float(label)
            else:
                sku_imp[sku] = 1
                sku_clk[sku] = float(label)
        label_list.append(label)
        pre_list.append(pre)

    f.close()


def main(predict_result_file):
    with open(predict_result_file, 'r') as result_file:
        cal_sctr_value(result_file)

        for key,value in sctr_map.items():
            sku=key.split('@')[1]
            if value[1] == 1:
                if sku in sku_sctr_imp:
                    sku_sctr_imp[sku] += 1
                    sku_sctr_clk[sku] += value[2]
                else:
                    sku_sctr_imp[sku] = 1
                    sku_sctr_clk[sku] = value[2]
        for key,value in sku_imp.items():
            if key in sku_sctr_imp:
                sctr_imp += value
                sctr_clk += sku_sctr_clk[key] / float(sku_sctr_imp[key]) * value
                sctr_ratio += float(sku_sctr_imp[key])
            else:
                sctr_imp += value
                sctr_clk += sku_clk[key]
                sctr_ratio += value
        print("sctr: ", sctr_clk/sctr_imp)
        
    


predict_result_file = 'predict_result.txt'
main(predict_result_file)
