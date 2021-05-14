import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#input_df = pd.read_csv('./uploaded_files/tmp.csv')
link_df = pd.read_csv('./nso_services/l3vpn_link.csv')
l2vpn_df = pd.read_csv('./nso_services/l2vpn.csv')

def write_to_file(df,unique_id):
    # file_out = r'c:\your_output_file_path\file_name.csv'
    # df.to_csv(file_out)
    # file_data = open(file_out, 'rb').read()
    # open(file_out, 'wb').write(file_data[:-2])
    file_out = 'interfaces_' + unique_id + '.txt'
    df.to_csv(file_out,index=False,header=False)
    file_data = open(file_out, 'rb').read()
    open(file_out, 'wb').write(file_data[:-1]) #change to -2 if IndexError

def hostname(unique_id):
    host_list = []
    try:
        input_df = pd.read_csv('./uploaded_files/tmp_' + unique_id + '.csv')
        host_c1 = input_df['HOSTNAME_C1']
        for _ in host_c1:
            if _ in host_list:
                continue
            else:
                host_list.append(_)
        return host_list # in list format
    except:
        return host_list

def final_out(host_list,unique_id):
    if not host_list:
        return {'error': 'File ' +'./uploaded_files/tmp_' + unique_id + '.csv'+' not found'}
    if 'infra' in unique_id or 'service' in unique_id:
        input_df = pd.read_csv('./uploaded_files/tmp_' + unique_id + '.csv')
        frame = []
        input_c1 = input_df[['HOSTNAME_C1','INTERFACE_C1']]
        frame.append(input_c1)
        input_c2 = input_df[['HOSTNAME_C2','INTERFACE_C2']]
        frame.append(input_c2)
    # elif 'services' in unique_id:
    #     frame = []
    #     for host in host_list:
    #         subset_1 = link_df[link_df['primary-link.device']==host]
    #         l3_pri = subset_1[['primary-link.device','primary-link.interface-id']]
    #         l3_pri = l3_pri.drop_duplicates()
    #         frame.append(l3_pri)
    #         subset_2 = link_df[link_df['secondary-link.device']==host]
    #         l3_sec = subset_2[['secondary-link.device','secondary-link.interface-id']]
    #         l3_sec = l3_sec.drop_duplicates()
    #         frame.append(l3_sec)
    #         subset_3 = l2vpn_df[l2vpn_df['elan.elan-sites.primary-link.device']==host]
    #         elan_pri = subset_3[['elan.elan-sites.primary-link.device','elan.elan-sites.primary-link.interface-id']]
    #         elan_pri = elan_pri.drop_duplicates()
    #         frame.append(elan_pri)
    #         subset_4 = l2vpn_df[l2vpn_df['elan.elan-sites.secondary-link.device']==host]
    #         elan_sec = subset_4[['elan.elan-sites.secondary-link.device','elan.elan-sites.secondary-link.interface-id']]
    #         elan_sec = elan_sec.drop_duplicates()
    #         frame.append(elan_sec)
    #         subset_5 = l2vpn_df[l2vpn_df['eline.eline-sites.primary-link.device']==host]
    #         eline_pri = subset_5[['eline.eline-sites.primary-link.device','eline.eline-sites.primary-link.interface-id']]
    #         eline_pri = eline_pri.drop_duplicates()
    #         frame.append(eline_pri)
    #         subset_6 = l2vpn_df[l2vpn_df['eline.eline-sites.secondary-link.device']==host]
    #         eline_sec = subset_6[['eline.eline-sites.secondary-link.device','eline.eline-sites.secondary-link.interface-id']]
    #         eline_sec = eline_sec.drop_duplicates()
    #         frame.append(eline_sec)
    # df = pd.DataFrame(np.concatenate((df1.values, df2.values), axis=0))
    # df.columns = ['a', 'x', 'y']
    # df
    final_frame = pd.DataFrame(np.concatenate((frame),axis=0))
    final_frame.columns = ['hostname','interface']
    # df.dropna(subset=["column2"], inplace=True)
    print(final_frame)
    final_frame.dropna(subset=['hostname'],inplace=True)
    final_frame.dropna(subset=['interface'],inplace=True)
    print(final_frame)
    write_to_file(final_frame,unique_id)

def parse_host_int(unique_id):
    host_input = hostname(unique_id)
    final_output  = final_out(host_input, unique_id)
    return (final_output)

if __name__ == '__main__':
    main()


