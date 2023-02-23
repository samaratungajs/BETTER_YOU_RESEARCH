
const timestamp = require('unix-timestamp');

export function unixConvertion(val){
    return timestamp.toDate(val)
}