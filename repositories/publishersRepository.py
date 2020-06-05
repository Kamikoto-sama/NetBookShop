from dataBaseContext import Publisher


class PublishersRepository:
	@staticmethod
	def addPublisher(publisherData: dict):
		publisherId = Publisher.create(**publisherData).userId
		publisher = list(Publisher.select().where(Publisher.id == publisherId))[0]
		return publisher

	@staticmethod
	def getPublishersByName(publisherName):
		publishers = Publisher.select().where(Publisher.name == publisherName).dicts()
		return list(publishers)
	
	@staticmethod
	def getAllPublishers():
		return list(Publisher.select().dicts())

	@staticmethod
	def updatePublisherById(publisherId, updatedValues: dict):
		Publisher.update(**updatedValues).where(Publisher.id == publisherId).execute()

	@staticmethod
	def deletePublisherById(publisherId):
		Publisher.delete_by_id(publisherId)