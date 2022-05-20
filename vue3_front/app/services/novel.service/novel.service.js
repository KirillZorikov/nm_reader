import axios from "axios";
import {constants} from '../../constants';

const API_URL = constants.API_URL;

class NovelService {
    async getListNovelsServices() {
        return await axios.get(API_URL + `novels/`);
    }
    async getListLanguages() {
        return await axios.get(API_URL + `novels/langs`);
    }
    async searchNovels(data, lang_code, service_name) {
        return await axios.post(API_URL + `novels/${lang_code}/${service_name}/search_page`, data);
    }
    async getDataFromLink(link, lang_code, service_name) {
        let urn = `novels/${lang_code}/${service_name}/from-url`
        if (typeof lang_code == 'undefined' && typeof service_name == 'undefined') {
            urn = 'novels/from-url'
        }
        return await axios.post(API_URL + urn, {
            url: link
        });
    }
    async getChapter(lang_code, service_name, novel_id, chapter_id) {
        return await axios.post(API_URL + `novels/${lang_code}/${service_name}/chapter_page`, {
            chapter_id: chapter_id,
            novel_id: novel_id,
        });
    }
}

export default new NovelService();