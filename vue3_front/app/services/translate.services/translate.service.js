import axios from "axios";
import {constants} from '../../constants'

const API_URL = constants.API_URL;

class TranslateService {
    async getTranslate(data, service_name) {
        return await axios.post(API_URL + `translate/${service_name}`, data);
    }
    async getListTranslateServices() {
        return await axios.get(API_URL + `translate/list`);
    }
    async initPages(service_name, count=4) {
        return await axios.post(API_URL + `parsers/pages/init`, {
            service_slug: service_name,
            pages_count: count,
        });
    }
}

export default new TranslateService();