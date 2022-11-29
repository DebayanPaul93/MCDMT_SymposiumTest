import streamlit as st

#user input

def paper_input():
	list_pH,list_intdp=[],[]
	original_title = '<p style="font-family:Sans serif; color:Cyan; font-size: 30px;"><b>Number of Collection Objects</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		objectno = st.number_input("Enter no. of objects",1,4)
	for counter in range (objectno):
		if(objectno>1):
			st.markdown("#### Type {} Object Chemical Properties".format(counter+1))
			colc, cold = st.columns(2)
			with colc:
				pH = st.slider("Select pH level",min_value=3,max_value=9,value=8,step=1,key='ph{}'.format(counter+1))
			with cold:
				int_dp = st.slider("Select Initial DP",min_value=500,max_value=2500,value=1200,step=50,key='dp{}'.format(counter+1))

			list_pH.append(pH)
			list_intdp.append(int_dp)

		else:
			st.markdown("#### Object Chemical Properties")
			cola, colb = st.columns(2)
			with cola:
				pH = st.slider("Select pH level",min_value=3,max_value=9,value=8,step=1,key='ph1')
			with colb:
				int_dp = st.slider("Select Initial DP",min_value=500,max_value=2500,value=1200,step=50,key='dp1')
			list_pH.append(pH)
			list_intdp.append(int_dp)

	original_title = '<p style="font-family:Sans serif; color:Cyan; font-size: 30px;"><b>Critical DP of Collection</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col10, col11, col12 = st.columns(3)
	with col10:
		crit_dp = st.slider("Select Critical DP",min_value=200,max_value=400,step=50)

