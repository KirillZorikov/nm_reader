import axios from "axios";
import {constants} from '../../constants'

const API_URL = constants.API_URL;

class ParserServices {
    async initPages(service_name, count=4) {
        return await axios.post(API_URL + `parsers/pages/init`, {
            service_slug: service_name,
            pages_count: count,
        });
    }
    async set_max_pages(service_name, count) {
        return await axios.post(API_URL + `parsers/set_max_pages`, {
            service_slug: service_name,
            pages_count: count,
        });
    }
    async set_timeout(service_name, timeout) {
        return await axios.post(API_URL + `parsers/set_timeout`, {
            service_slug: service_name,
            timeout: timeout,
        });
    }
}

export default new ParserServices();