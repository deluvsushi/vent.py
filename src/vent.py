import requests
from datetime import datetime

class Vent:
	def __init__(self) -> None:
		self.api = "https://api.ventfeed.com/api"
		self.headers = {
			"user-agent": "okhttp/3.12.13",
			"x-3po": "2060aeb1e074f6d3fa27bbb729e7ff91ab27bfbb",
			"x-app-version": "android;5.0.23(23530000)",
			"x-device-hardware": "Asus ASUS_Z01QD",
			"x-device-os-version": "7.1.2(25)",
			"x-ob1": "3cc9c10db7796114535eee6383ff1b8ec3152fdc",
			"x-user-platform": "android"
		}
		self.user_id = None
		self.username = None
		self.auth_token = None


	def login(self, username: str, password: str) -> dict:
		data = {
			"user": {
				"username": username,
				"password": password
			}
		}
		response = requests.post(
			f"{self.api}/v1/sign_in",
			json=data,
			headers=self.headers).json()
		if "user" in response:
			self.user_id = response["user"]["id"]
			self.username = response["user"]["username"]
			self.auth_token = response["user"]["authentication_token"]
			self.headers["x-user-token"] = self.auth_token
			self.headers["x-user-username"] = self.username
		return response

	def register(
			self,
			username: str,
			password: str,
			email: str) -> dict:
		data = {
			"user": {
				"username": username,
				"password": password,
				"email": email
			}
		}
		return requests.post(
			f"{self.api}/v1/registrations",
			json=data,
			headers=self.headers).json()

	def get_interests(
			self,
			per_page: int = 25,
			order: str = "asc",
			field: str = "name") -> dict:
		return requests.get(
			f"{self.api}/v1/interests?per_page={per_page}&from[order]={order}&from[field]={field}",
			headers=self.headers).json()

	def get_suggested_groups(self, per_page: int = 30) -> dict:
		return requests.get(
			f"{self.api}/v1/suggested_groups?per_page={per_page}",
			headers=self.headers).json()

	def listen_group(self, group_id: str, from_suggested_groups: bool = False) -> dict:
		return requests.post(
			f"{self.api}/v1/groups/{group_id}/listen?from_suggested_groups={from_suggested_groups}",
			headers=self.headers).json()

	def unlisten_group(self, group_id: str, from_suggested_groups: bool = False) -> dict:
		return requests.delete(
			f"{self.api}/v1/groups/{group_id}/unlisten?from_suggested_groups={from_suggested_groups}",
			headers=self.headers).json()


	def get_user_info(self, user_id: str) -> dict:
		return requests.get(
			f"{self.api}/v1/users/{user_id}",
			headers=self.headers).json()

	def get_backgrounds_list(self) -> dict:
		return requests.get(
			f"{self.api}/v1/backgrounds",
			headers=self.headers).json()

	def get_emotion_categories(self) -> dict:
		return requests.get(
			f"{self.api}/v1/emotion_categories",
			headers=self.headers).json()

	def get_interaction_types(self) -> dict:
		return requests.get(
			f"{self.api}/v2/interaction_types",
			headers=self.headers).json()

	def get_notifications_count(self) -> dict:
		return requests.get(
			f"{self.api}/v1/my/notifications/notifications_count",
			headers=self.headers).json()

	def get_latest_vents(
			self,
			per_page: int = 10,
			order: str = "desc",
			field: str = "created_at") -> dict:
		return requests.get(
			f"{self.api}/v2/vents/latest?per_page={per_page}&from[order]={order}&from[field]={field}&from[value]={datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z",
			headers=self.headers).json()

	def listen_user(self, user_id: str) -> dict:
		return requests.post(
			f"{self.api}/v1/users/{user_id}/listen",
			headers=self.headers).json()

	def unlisten_user(self, user_id: str) -> dict:
		return requests.delete(
			f"{self.api}/v1/users/{user_id}/unlisten",
			headers=self.headers).json()

	def get_user_vents(
			self,
			user_id: str,
			per_page: int = 10,
			order: str = "desc",
			field: str = "created_at") -> dict:
		return requests.get(
			f"{self.api}/v2/vents?q[user_id_eq]={user_id}&per_page={per_page}&from[order]={order}&from[field]={field}",
			headers=self.headers).json()

	def get_user_followers(
			self,
			user_id: str,
			per_page: int = 25) -> dict:
		return requests.get(
			f"{self.api}/v1/users/{user_id}/followers?per_page={per_page}",
			headers=self.headers).json()

	def get_user_followings(
			self,
			user_id: str,
			per_page: int = 25) -> dict:
		return requests.get(
			f"{self.api}/v1/users/{user_id}/followings?per_page={per_page}",
			headers=self.headers).json()

	def get_user_interactions(
			self,
			user_id: str,
			per_page: int = 10) -> dict:
		return requests.get(
			f"{self.api}/v2/users/{user_id}/vents/interacted?per_page={per_page}",
			headers=self.headers).json()

	def comment_vent(
			self,
			vent_id: str,
			comment: str) -> dict:
		data = {
			"comment": {
				"body": comment
			}
		}
		return requests.post(
			f"{self.api}/v1/vents/{vent_id}/comments",
			json=data,
			headers=self.headers).json()

	def edit_comment(
			self,
			vent_id: str,
			comment_id: str,
			comment: str) -> dict:
		data = {
			"comment": {
				"body": comment
			}
		}
		return requests.put(
			f"{self.api}/v1/vents/{vent_id}/comments/{comment_id}",
			json=data,
			headers=self.headers).json()
	
	def delete_comment(
			self,
			vent_id: str,
			comment_id: str) -> int:
		return requests.delete(
			f"{self.api}/v1/vents/{vent_id}/comments/{comment_id}",
			headers=self.headers).status_code

	def get_report_reasons(self, object_type: int = 0) -> dict:
		return requests.get(
			f"{self.api}/v1/report_reasons?q[object_type_eq]={object_type}",
			headers=self.headers).json()

	def report_vent(
			self,
			vent_id: str,
			comment: str,
			reason_id: str) -> dict:
		data = {
			"comment": comment,
			"report_reason_id": reason_id
		}
		return requests.post(
			f"{self.api}/v1/vents/{vent_id}/reports",
			json=data,
			headers=self.headers).json()

	def subscript_user(self, user_id: str) -> dict:
		return requests.post(
			f"{self.api}/v1/users/{user_id}/user_subscriptions",
			headers=self.headers).json()

	def unsubscript_user(self, user_id: str) -> dict:
		return requests.delete(
			f"{self.api}/v1/users/{user_id}/user_subscriptions",
			headers=self.headers).json()

	def get_user_public_url(self, user_id: str) -> dict:
		return requests.get(
			f"{self.api}/v1/users/{user_id}/public_url",
			headers=self.headers).json()

	def block_user(self, user_id: str) -> dict:
		return requests.post(
			f"{self.api}/v1/users/{user_id}/block",
			headers=self.headers).json()

	def unblock_user(self, user_id: str) -> dict:
		return requests.delete(
			f"{self.api}/v1/users/{user_id}/unblock",
			headers=self.headers).json()

	def report_user(
			self,
			user_id: str,
			comment: str,
			reason_id: str) -> dict:
		data = {
			"comment": comment,
			"report_reason_id": reason_id
		}
		return requests.post(
			f"{self.api}/v1/users/{user_id}/reports",
			json=data,
			headers=self.headers).json()

	def get_group_info(self, group_id: str) -> dict:
		return requests.get(
			f"{self.api}/v1/groups/{group_id}",
			headers=self.headers).json()

	def get_group_latest_vents(
			self,
			group_id: str,
			per_page: int = 10,
			order: str = "desc",
			field: str = "created_at") -> dict:
		return requests.get(
			f"{self.api}/v2/groups/{group_id}/vents?per_page={per_page}&from[order]={order}&from[field]={field}&from[value]={datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z",
			headers=self.headers).json()

	def get_group_trending_vents(self, group_id: str, per_page: int = 10) -> dict:
		return requests.get(
			f"{self.api}/v2/groups/{group_id}/vents/on_the_rise?per_page={per_page}",
			headers=self.headers).json()

	def mute_group(self, group_id: str) -> dict:
		return requests.post(
			f"{self.api}/v1/groups/{group_id}/mute",
			headers=self.headers).json()

	def unmute_group(self, group_id: str) -> dict:
		return requests.delete(
			f"{self.api}/v1/groups/{group_id}/unmute",
			headers=self.headers).json()

	def report_group(
			self,
			group_id: str,
			comment: str,
			reason_id: str) -> dict:
		data = {
			"comment": comment,
			"report_reason_id": reason_id
		}
		return requests.post(
			f"{self.api}/v1/groups/{group_id}/reports",
			json=data,
			headers=self.headers).json()

	def create_vent(
			self,
			emotion_id: str,
			content: str,
			city: str = None,
			group_id: str = None,
			comment_setting: str = "comments_enabled",
			privacy_setting: str = "privacy_public") -> dict:
		data = {
			"vent": {
				"emotion_id": emotion_id,
				"body": content,
				"comment_setting": comment_setting,
				"privacy_setting": privacy_setting
			}
		}
		if city:
			data["vent"]["city"] = city
		if group_id:
			data["vent"]["group_id"] = group_id
		return requests.post(
			f"{self.api}/v1/my/vents",
			json=data,
			headers=self.headers).json()

	def edit_vent(
			self,
			vent_id: str,
			emotion_id: str,
			content: str,
			city: str = None,
			group_id: str = None,
			comment_setting: str = "comments_enabled",
			privacy_setting: str = "privacy_public") -> dict:
		data = {
			"vent": {
				"emotion_id": emotion_id,
				"body": content,
				"comment_setting": comment_setting,
				"privacy_setting": privacy_setting
			}
		}
		if city:
			data["vent"]["city"] = city
		if group_id:
			data["vent"]["group_id"] = group_id
		return requests.put(
			f"{self.api}/v1/my/vents/{vent_id}",
			json=data,
			headers=self.headers).json()

	def delete_vent(self, vent_id: str) -> int:
		return requests.delete(
			f"{self.api}/v1/my/vents/{vent_id}",
			headers=self.headers).status_code

	def get_listened_groups(
			self,
			per_page: int = 15,
			order: str = "desc",
			field: str = "last_vented_at") -> dict:
		return requests.get(
			f"{self.api}/v1/my/groups?per_page={per_page}&from[order]={order}&from[field]={field}&from[value]=9999-01-01T00:00:00.000Z",
			headers=self.headers).json()

	def get_account_feed(
			self,
			per_page: int = 15,
			order: str = "desc",
			field: str = "created_at") -> dict:
		return requests.get(
			f"{self.api}/v2/my/feed?per_page={per_page}&from[order]={order}&from[field]={field}&from[value]=9999-01-01T00:00:00.000Z",
			headers=self.headers).json()

	def create_group(
			self,
			group_name: str,
			description: str,
			interest_ids: list,
			is_nsfw: bool = False,
			color: str = "#000000") -> dict:
		data = {
			"group": {
				"name": group_name,
				"bio": description,
				"is_nsfw": is_nsfw,
				"color": color,
				"interest_ids": interest_ids
			}
		}
		return requests.post(
			f"{self.api}/v1/groups",
			json=data,
			headers=self.headers).json()


	def edit_group(
			self,
			group_id:  str,
			group_name: str,
			description: str,
			interest_ids: list,
			is_nsfw: bool = False,
			color: str = "#000000") -> dict:
		data = {
			"group": {
				"name": group_name,
				"bio": description,
				"is_nsfw": is_nsfw,
				"color": color,
				"interest_ids": interest_ids
			}
		}
		return requests.put(
			f"{self.api}/v1/groups/{group_id}",
			json=data,
			headers=self.headers).json()

	def delete_group(self, group_id: str) -> int:
		return requests.delete(
			f"{self.api}/v1/groups/{group_id}",
			headers=self.headers).status_code

	def get_group_followers(self, group_id: str,  per_page: int = 25) -> dict:
		return requests.get(
			f"{self.api}/v1/groups/{group_id}/followers?per_page={per_page}",
			headers=self.headers).json()

	def get_group_blocked_followers(self, group_id: str,  per_page: int = 25) -> dict:
		return requests.get(
			f"{self.api}/v1/groups/{group_id}/followers/blocked?per_page={per_page}",
			headers=self.headers).json()

	def get_notifications_subscriptions(self) -> dict:
		return requests.get(
			f"{self.api}/v1/my/notifications/subscriptions",
			headers=self.headers).json()

	def get_user_notifications_list(
			self,
			per_page: int = 10,
			order: str = "desc",
			field: str = "last_activity_at") -> dict:
		return requests.get(
			f"{self.api}/v1/my/user_notifications?per_page={per_page}&from[order]={order}&from[field]={field}&from[value]=9999-01-01T00:00:00.000Z",
			headers=self.headers).json()

	def get_system_notifications_list(
			self,
			per_page: int = 10,
			order: str = "desc",
			field: str = "last_activity_at") -> dict:
		return requests.get(
			f"{self.api}/v1/my/system_notifications?per_page={per_page}&from[order]={order}&from[field]={field}&from[value]=9999-01-01T00:00:00.000Z",
			headers=self.headers).json()

	def mark_notifications_read(self, notification_ids: list) -> dict:
		data = {
			"ids": notification_ids
		}
		return requests.put(
			f"{self.api}/v1/my/notifications/mark_read",
			json=data,
			headers=self.headers).json()

	def get_listen_requests(self) -> dict:
		return requests.get(
			f"{self.api}/v1/my/listen_requests",
			headers=self.headers).json()

	def start_conversation(self, user_id: str) -> dict:
		data = {
			"conversation": {
				"user_id": user_id
			}
		}
		return requests.post(
			f"{self.api}/v2/my/conversations",
			json=data,
			headers=self.headers).json()

	def get_suggested_users(self) -> dict:
		return requests.get(
			f"{self.api}/v1/users/suggested",
			headers=self.headers).json()

	def edit_profile(
			self,
			profile_image_url: str = None,
			username: str = None,
			bio: str = None,
			birthday: str = "1994-04-04",
			nsfw_setting: str = "collapse",
			account_is_public: int = 1,
			has_private_bio: int = 0) -> dict:
		data = {}
		if profile_image_url:
			data["user"]["profile_image_url"] = profile_image_url
		if username:
			data["user"]["username"] = username
		if bio:
			data["user"]["bio"] = bio
		if birthday:
			data["user"]["dob"] = birthday
		if nsfw_setting:
			data["user"]["nsfw_setting"] = nsfw_setting
		if account_is_public:
			data["user"]["account_is_public"] = account_is_public
		if has_private_bio:
			data["user"]["has_private_bio"] = has_private_bio
		return requests.put(
			f"{self.api}/v1/my/user",
			json=data,
			headers=self.headers).json()

	def reset_password(self, email: str) -> dict:
		data = {"email": email}
		return requests.post(
			f"{self.api}/v1/forgot-password",
			json=data,
			headers=self.headers).json()

	def resend_email_confirmation(self) -> dict:
		return requests.post(
			f"{self.api}/v1/my/user/resend_confirmation",
			headers=self.headers).json()

	def change_password(self, password: str) -> dict:
		data = {
			"user": {
				"password": password
			}
		}
		return requests.put(
			f"{self.api}/v1/my/user",
			json=data,
			headers=self.headers).json()

	def get_blocked_users(self, per_page: int = 25) -> dict:
		return requests.get(
			f"{self.api}/v1/my/inverse_blockings?per_page={per_page}",
			headers=self.headers).json()

	def deactivate_account(self) -> int:
		return requests.delete(
			f"{self.api}/v1/my/user",
			headers=self.headers).status_code
