# encoding=utf8
import xmltodict
import csv
import requests
from datetime import date

#adapt for lambda: https://stackoverflow.com/questions/49695050/write-csv-file-and-save-it-into-s3-using-aws-lambda-python

pullremote = "t"

if (pullremote == "t"):
	dataurl = "https://www.reginfo.gov/public/do/PRAXML?type=inventory"
	print("Beginning XML Download")
	r = requests.get(dataurl, allow_redirects=True)
	print("Downloaded Successfully")
	doc = xmltodict.parse(r.content)
	print("Loaded XML File")

else:
	with open('CurrentInventoryReport.xml') as fd:
		doc = xmltodict.parse(fd.read())
		print("Loaded XML File")


outfile = "current-inventory-report-"+date.today().strftime("%m-%d-%y")+".csv"
print(outfile)

with open(outfile, 'w') as csvfile:
	fieldnames = ['omb_number', 'icr_reference_number', 'agency_code', 'title', 'abstract', 'pii_flag', 'expiration_date', 'totalresponse_quantity', 'totalresponse_hours', 'totalresponse_cost', 'agencycontact_firstname', 'agencycontact_lastname', 'agencycontact_email', 'agencycontact_phone', 'link']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()

	for x in doc['InformationCollectionRequestList']['InformationCollectionRequest']:
		icr_container = {}
		
		# print(x,"\n\n")

		try:
			icr_container['omb_control_num'] = x['OMBControlNumber']
		except KeyError:
			pass

		try:
			icr_container['icr_ref_num'] = x['ICRReferenceNumber']
		except KeyError:
			pass

		try:
			icr_container['agency_code'] = x['AgencyCode']
		except KeyError:
			icr_container['agency_code'] = ""
			pass


		try:
			icr_container['title'] = x['Title']
		except KeyError:
			pass

		try:
			icr_container['abstract'] = x['Abstract']
		except KeyError:
			icr_container['abstract'] = ""
			pass

		try:
			icr_container['pii'] = x['PIIFlag']
		except KeyError:
			icr_container['pii'] = ""
			pass

		try:
			icr_container['expiration_date'] = x['Expiration']['ExpirationDate']
		except KeyError:
			icr_container['expiration_date'] = ""
			pass

		try:
			icr_container['totalresponse_quantity'] = x['Burden']['BurdenResponse']['TotalQuantity']
		except KeyError:
			icr_container['totalresponse_quantity'] = ""
			pass

		try:
			icr_container['totalresponse_hours'] = x['Burden']['BurdenHour']['TotalQuantity']
		except KeyError:
			icr_container['totalresponse_hours'] = ""
			pass

		try:
			icr_container['totalresponse_cost'] = x['Burden']['BurdenCost']['TotalAmount']
		except KeyError:
			icr_container['totalresponse_cost'] = ""
			pass

		try:
			icr_container['agencycontact_firstname'] = x['AgencyContact']['Person']['FirstName']
		except KeyError:
			icr_container['agencycontact_firstname'] = ""
			pass

		try:
			icr_container['agencycontact_lastname'] = x['AgencyContact']['Person']['LastName']
		except KeyError:
			icr_container['agencycontact_lastname'] = ""
			pass
		
		try:
			icr_container['agencycontact_email'] = x['AgencyContact']['Person']['ElectronicAddress']
		except KeyError:
			icr_container['agencycontact_email'] = ""
			pass
		
		try:
			icr_container['agencycontact_phone'] = x['AgencyContact']['Person']['PhoneNumber']
		except KeyError:
			icr_container['agencycontact_phone'] = ""
			pass
		
		except KeyError:
			print("error")
			pass

		#Note: Each ICR can have more than one form associated with it. More data can be extracted for presentation output, but conceptually depulicative of the main ICR metadata
		# try:
		# 	for key, payload in x['InformationCollections'].items():
		# 		i = 0
		# 		j = 0

		# 		for y in payload:
		# 			try:
		# 				icr_container['forms'][i]['title'] = y['Title']

		# 				print(len(icr_container['forms']))
		# 			except KeyError:
		# 				pass

		# 			try:
		# 				icr_container['forms'][i]['ObligationCode'] = y['ObligationCode']
		# 			except KeyError:
		# 				pass
					
		# 			try:
		# 				icr_container['forms'][i]['LineOfBusiness'] = y['FEABusinessReferenceModule']['LineOfBusiness']['#text']
		# 			except KeyError:
		# 				pass
					
		# 			try:
		# 				icr_container['forms'][i]['Subfunction'] = y['FEABusinessReferenceModule']['Subfunction']['#text']
		# 			except KeyError:
		# 				pass
					
		# 			try:
		# 				icr_container['forms'][i]['AffectedPublicCode'] = y['AffectedPublicCode']['PublicCode']
		# 			except KeyError:
		# 				pass
					
		# 			try:
		# 				icr_container['forms'][i]['AnnualNumberResponses'] = y['NumberResponses']['AnnualQuantity']
		# 			except KeyError:
		# 				pass
					
		# 			try:
		# 				icr_container['forms'][i]['AnnualTotalHours'] = y['BurdenHour']['TotalQuantity']
		# 			except KeyError:
		# 				pass
					
		# 			try:
		# 				icr_container['forms'][i]['AnnualTotalCost'] =  y['BurdenCost']['TotalAmount']
		# 			except KeyError:
		# 				pass
					
		# 			try:
		# 				for key, instrument in y['Instruments'].items():
		# 					if(instrument['FormName']):
		# 						icr_container['forms'][i]['instruments'][j][FormName] = instrument['FormName']
		# 						if(instrument['FormNumber']):
		# 							icr_container['forms'][i]['instruments'][j][FormNumber] = instrument['FormNumber']
		# 						j+=1
		# 			except KeyError:
		# 				pass
					
		# 			i+=1

		##except Exception as e: print(e)
		# except:
		# 	# print("wah wah\n\n\n")
		# 	pass

		
		try:			
			link = "https://www.reginfo.gov/public/do/PRAViewRCF?ref_nbr=" + icr_container['icr_ref_num']

			row = {
				'omb_number' : icr_container['omb_control_num'],
				'icr_reference_number' : icr_container['icr_ref_num'],
				'agency_code' : icr_container['agency_code'],
				'title' : icr_container['title'],
				'abstract' : icr_container['abstract'],
				'pii_flag' : icr_container['pii'],
				'expiration_date' : icr_container['expiration_date'],
				'totalresponse_quantity' : icr_container['totalresponse_quantity'],
				'totalresponse_hours' : icr_container['totalresponse_hours'],
				'totalresponse_cost' : icr_container['totalresponse_cost'] ,
				'agencycontact_firstname' : icr_container['agencycontact_firstname'],
				'agencycontact_lastname' : icr_container['agencycontact_lastname'], 
				'agencycontact_email' : icr_container['agencycontact_email'],
				'agencycontact_phone' : icr_container['agencycontact_phone'],
				'link': link
				}	

			writer.writerow(row)
		
		except Exception as e: print(e)
		# except:
		# 	print("cant make row!")
		# 	pass








# Illustrative collection request
# <InformationCollectionRequest>
#         <OMBControlNumber>0503-0007</OMBControlNumber>
#         <ICRReferenceNumber>201708-0503-002</ICRReferenceNumber>
#         <AgencyCode>0503</AgencyCode>
#         <Title>National Appeals Division Customer Service Survey</Title>
#         <Abstract>To conduct a customer survey to gather date on the quality of how to make improvements in NAD processes and establish customer service standards.       </Abstract>
#         <ICRTypeCode>Revision of a currently approved collection</ICRTypeCode>
#         <Expiration>
#             <ExpirationDate>2020-10-31-04:00</ExpirationDate>
#         </Expiration>
#         <ICRStatus>Active</ICRStatus>
#         <AgencyContact>
#             <Person>
#                 <FirstName>Jerry</FirstName>
#                 <MiddleName>L</MiddleName>
#                 <LastName>Jobe</LastName>
#                 <PhoneNumber>703 305-2514</PhoneNumber>
#             </Person>
#         </AgencyContact>
#         <PIIFlag>No</PIIFlag>
#         <PrivacyActStatementFlag>No</PrivacyActStatementFlag>
#         <AnnualFederalCostAmount>62810</AnnualFederalCostAmount>
#         <StimulusIndicator>No</StimulusIndicator>
#         <HealthcareIndicator>No</HealthcareIndicator>
#         <DoddFrankActIndicator>No</DoddFrankActIndicator>
#         <AuthorizingStatutes>
#             <AuthorizingStatute>
#                 <ExecutiveOrder>
#                     <EONumber>12862</EONumber>
#                     <NameOfEO>Setting Customer Service Standards</NameOfEO>
#                 </ExecutiveOrder>
#             </AuthorizingStatute>
#         </AuthorizingStatutes>
#         <Burden>
#             <BurdenResponse>
#                 <TotalQuantity>2400</TotalQuantity>
#                 <PreviousTotalQuantity>2400</PreviousTotalQuantity>
#             </BurdenResponse>
#             <BurdenHour>
#                 <TotalQuantity>353</TotalQuantity>
#                 <PreviousTotalQuantity>353</PreviousTotalQuantity>
#             </BurdenHour>
#             <BurdenCost>
#                 <TotalAmount>0</TotalAmount>
#                 <PreviousTotalAmount>0</PreviousTotalAmount>
#             </BurdenCost>
#         </Burden>
#         <InformationCollections>
#             <InformationCollection>
#                 <Title>National Appeals Division Customer Service Survey</Title>
#                 <StandardFormIndicator>No</StandardFormIndicator>
#                 <ObligationCode>Voluntary</ObligationCode>
#                 <FEABusinessReferenceModule>
#                     <LineOfBusiness Code="116">Litigation and Judicial Activities</LineOfBusiness>
#                     <Subfunction Code="055">Resolution Facilitation</Subfunction>
#                 </FEABusinessReferenceModule>
#                 <Instruments>
#                     <Instrument>
#                         <FormNumber>None</FormNumber>
#                         <FormName>NAD Customer Survey</FormName>
#                         <AvailableElectronically>No</AvailableElectronically>
#                         <ElectronicCapability>Printable Only</ElectronicCapability>
#                         <InstrumentDocument>
#                             <documentType>Form</documentType>
#                         </InstrumentDocument>
#                     </Instrument>
#                 </Instruments>
#                 <AffectedPublicCode>
#                     <PublicCode>Individuals or Households</PublicCode>
#                 </AffectedPublicCode>
#                 <NumberResponses>
#                     <AnnualQuantity>2000</AnnualQuantity>
#                 </NumberResponses>
#                 <BurdenHour>
#                     <TotalQuantity>333</TotalQuantity>
#                     <BurdenHourPerResponse>
#                         <ReportingFrequencies>
#                             <ReportingFrequency>Annually</ReportingFrequency>
#                         </ReportingFrequencies>
#                     </BurdenHourPerResponse>
#                 </BurdenHour>
#                 <BurdenCost>
#                     <TotalAmount>0</TotalAmount>
#                 </BurdenCost>
#             </InformationCollection>
#             <InformationCollection>
#                 <Title>National Appeals Division Customer Service Survey Non-Respondents</Title>
#                 <StandardFormIndicator>No</StandardFormIndicator>
#                 <ObligationCode>Voluntary</ObligationCode>
#                 <FEABusinessReferenceModule>
#                     <LineOfBusiness Code="116">Litigation and Judicial Activities</LineOfBusiness>
#                     <Subfunction Code="055">Resolution Facilitation</Subfunction>
#                 </FEABusinessReferenceModule>
#                 <Instruments>
#                     <Instrument>
#                         <FormNumber>None</FormNumber>
#                         <FormName>NAD Customer Survey</FormName>
#                         <AvailableElectronically>No</AvailableElectronically>
#                         <ElectronicCapability>Printable Only</ElectronicCapability>
#                         <InstrumentDocument>
#                             <documentType>Form</documentType>
#                         </InstrumentDocument>
#                     </Instrument>
#                 </Instruments>
#                 <AffectedPublicCode>
#                     <PublicCode>Individuals or Households</PublicCode>
#                 </AffectedPublicCode>
#                 <NumberResponses>
#                     <AnnualQuantity>400</AnnualQuantity>
#                 </NumberResponses>
#                 <BurdenHour>
#                     <TotalQuantity>20</TotalQuantity>
#                     <BurdenHourPerResponse>
#                         <ReportingFrequencies>
#                             <ReportingFrequency>Annually</ReportingFrequency>
#                         </ReportingFrequencies>
#                     </BurdenHourPerResponse>
#                 </BurdenHour>
#                 <BurdenCost>
#                     <TotalAmount>0</TotalAmount>
#                 </BurdenCost>
#             </InformationCollection>
#         </InformationCollections>
#         <OIRAConclusion>
#             <ConcludedDate>
#                 <Date>2017-10-19-04:00</Date>
#                 <Time>03:41:10.576-04:00</Time>
#             </ConcludedDate>
#         </OIRAConclusion>
#     </InformationCollectionRequest>
