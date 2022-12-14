import streamlit as st,pandas as pd,os, math
import streamlit_ext as ste

#user input

def paper_input():
	list_pH,list_intdp=[],[]
	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Collection Objects Details</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		objectno = ste.number_input("Enter number of type of objects",1,4,key='noofobjecttype')
	for counter in range (objectno):
		if(objectno>1):
			st.markdown("#### Type {} Object Chemical Properties".format(counter+1))
			colc, cold = st.columns(2)
			with colc:
				pH = ste.slider("Select pH level",min_value=3,max_value=9,value=8,step=1,key='ph{}'.format(counter+2))
			with cold:
				int_dp = ste.slider("Select Initial DP",min_value=500,max_value=2500,value=1200,step=50,key='dp{}'.format(counter+2))

			if isinstance(pH, tuple):
				pH = pH[0]
			if isinstance(int_dp, tuple):
				int_dp = int_dp[0]

			list_pH.append(pH)
			list_intdp.append(int_dp)

		else:
			st.markdown("#### Object Chemical Properties")
			cola, colb = st.columns(2)
			with cola:
				pH = ste.slider("Select pH level",min_value=3,max_value=9,value=8,step=1,key='ph1')
			with colb:
				int_dp = ste.slider("Select Initial DP",min_value=500,max_value=2500,value=1200,step=50,key='dp1')

			if isinstance(pH, tuple):
				pH = pH[0]
			if isinstance(int_dp, tuple):
				int_dp = int_dp[0]

			list_pH.append(pH)
			list_intdp.append(int_dp)

	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Critical DP of Collection</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col10, col11, col12 = st.columns(3)
	with col10:
		crit_dp = ste.slider("Select Critical DP",min_value=200,max_value=400,step=50,key='critdp')
		if isinstance(crit_dp, tuple):
			crit_dp = crit_dp[0]

	for i in range(3):
		st.write("")
	save = st.checkbox('Save Inputs (*)', value=False, key='papersave')


	if save:
		valuelist = [objectno,list_pH,list_intdp,crit_dp]
		columnlist = ['Number of object types', 'List of pH Values', 'List of Initial DP Values', 'Critical DP']


		#Current working directory
		cwd = os.getcwd()
		#set path to subdirectory and inputfilename
		inputfilesnamewithpath = cwd+'\\Inputfiles\\PaperUserInputs.csv'

		#Write the inputs to a csv file
		inputdf = pd.DataFrame([valuelist], columns = columnlist)

		inputdf.to_csv(inputfilesnamewithpath, index=False)


