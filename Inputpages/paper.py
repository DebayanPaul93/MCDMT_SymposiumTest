import streamlit as st

#user input

def paper_input():
	list_pH,list_intdp,list_percent=[],[],[]
	original_title = '<p style="font-family:Sans serif; color:Cyan; font-size: 30px;"><b>Number of Collection Objects</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		objectno = st.number_input("Enter no. of objects",1,4)
	for counter in range (objectno):
		if(objectno>1):
			st.markdown("#### Type {} Object Chemical Properties".format(counter+1))
			#if(objectno == 2):
			colc, cold, cole = st.columns(3)
			with colc:
				pH = st.slider("Select pH level",min_value=3,max_value=9,value=8,step=1,key='ph{}'.format(counter+1))
			with cold:
				int_dp = st.slider("Select Initial DP",min_value=500,max_value=2500,value=1200,step=50,key='dp{}'.format(counter+1))
			with cole:
				col_perct = st.slider("Select % of Object {} in Collection".format(counter+1),min_value=10,max_value=100,step=10,key='percent{}'.format(counter+1))

			list_pH.append(pH)
			list_intdp.append(int_dp)
			list_percent.append(col_perct)

		else:
			st.markdown("#### Object Chemical Properties")
			cola, colb = st.columns(2)
			with cola:
				pH = st.slider("Select pH level",min_value=3,max_value=9,value=8,step=1,key='ph1')
			with colb:
				int_dp = st.slider("Select Initial DP",min_value=500,max_value=2500,value=1200,step=50,key='dp1')
			col_perct = 100
			list_pH.append(pH)
			list_intdp.append(int_dp)
			list_percent.append(col_perct)

	#Sum check 
	if(sum(list_percent)!=100):
		st.warning("The sum of all percentages should be 100 in case of multiple objects")

	original_title = '<p style="font-family:Sans serif; color:Cyan; font-size: 30px;"><b>Critical DP of Collection</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col10, col11, col12 = st.columns(3)
	with col10:
		crit_dp = st.slider("Select Critical DP",min_value=200,max_value=400,step=50)

