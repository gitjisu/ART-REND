const AUTH = 'auth-service/'
const BUSINESS = 'business-service/'
const RECOMMEND = 'recommend-service/'

export default {
	auth: {
		kakaoLogin: () => `${AUTH}oauth2/authorization/kakao`,
		nickNameForm: memberId => `${AUTH}signup/${memberId}/nickname`,
		nickNameCheck: memberId => `${AUTH}signup/${memberId}/nickname/duplicate`,
	},
	business: {
		select: () => `${BUSINESS}api/select`,
		detail: (artworkId, memberId) =>
			`${BUSINESS}api/paintings/${artworkId}/${memberId}`,
		like: () => `${BUSINESS}api/like`,
		getHits: () => `${BUSINESS}api/paintings/sort`,
		getArtisDetail: () => `${BUSINESS}api/paintings/search`,
	},
	recommend: {
		mainpage: () => `${RECOMMEND}api/v1/painting/main_recommend_painting/`,
	},
}