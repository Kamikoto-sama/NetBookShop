from dataBaseContext import Publisher


class PublishersRepository:
	@staticmethod
	def addPublisher(publisherData: dict):
		Publisher.create(**publisherData)

	@staticmethod
	def getPublisherByName(publisherName):
		publisher = Publisher.select().where(Publisher.name == publisherName).dicts().first()
		return publisher
	
	@staticmethod
	def getAllPublishers():
		return list(Publisher.select().dicts())

	@staticmethod
	def updatePublisherById(publisherId, updatedValues: dict):
		Publisher.update(**updatedValues).where(Publisher.id == publisherId).execute()

	@staticmethod
	def deletePublisherById(publisherId):
		Publisher.delete_by_id(publisherId)