


label_list = []
pre_list = []
sctr_map = {}
sku_imp = {}
sku_clk = {}
sku_sctr_imp = {}
sku_sctr_clk = {}

def cal_sctr_value(result_file_path):
    global sctr_map
    with open(result_file_path, 'r') as result_lines:
        all_lines = result_lines.readlines()
    
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

    result_lines.close()


def main(predict_result_file):
    cal_sctr_value(predict_result_file)

    nsctr_imp = 0.0
    nsctr_clk = 0.0
    nsctr_ratio = 0.0

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
            nsctr_imp += value
            nsctr_clk += sku_sctr_clk[key] / float(sku_sctr_imp[key]) * value
            nsctr_ratio += float(sku_sctr_imp[key])
        else:
            nsctr_imp += value
            nsctr_clk += sku_clk[key]
            nsctr_ratio += value
    print("nsctr: ", nsctr_clk/nsctr_imp)
        
predict_result_file = 'nsctr_test_data'
main(predict_result_file)
