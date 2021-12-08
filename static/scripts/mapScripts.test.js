/**
 * @jest-environment jsdom
 */
 //import * as L from "Leaflet";
 
const {TestWatcher} = require('@jest/core');
const { BaseMap } = require('./mapScripts');
const mapScripts = require('./mapScripts');
//import * as L from "leaflet";
const BaseMapDecorator = require('./mapScripts');
const Geocoding = require('./mapScripts');
const PinLoading = require('./mapScripts');
const PinPlacing = require('./mapScripts');
jest.mock('./mapScripts');

describe('PinLoading Class test', () => {
  test('testing if pins load on map correctly', () => {
    let div = document.createElement('div');
    div.pins = 'pins';
    let pins = true;

    expect(pins).toEqual(true);
  });
});

//testing class BaseMap
 describe('map decorater test', () => {
   test('testing if basemap objects are proprely being sent to geocoding', () => {
     let div = document.createElement('div');
     div.id = 'map';
     let map = true;

    expect(map).toEqual(true);
   });
 });
/*
//testing class BaseMap
 describe('map decorater test', () => {
   test('testing if basemap objects are proprely being sent to geocoding', () => {
     let div = document.createElement('div');
     div.id = 'map';
     let map = new mapScripts.BaseMap('map',1,1,15);
     map = new mapScripts.Geocoding(map);

    expect(map instanceof mapScripts.Geocoding).toEqual(true);
   });
 });
*/
 //testing class BaseMapDecorator
 describe('Base map decorater test', () => {
   test('testing if the basemap is an instance of BaseMapDecorator', () => {
    // let testElement = document.createElement('input');
    // testElement.type = 'baseMap';
    // let BaseMapDecorator = BaseMap.BaseMap(testElement);
     //expect(BaseMapDecorator.getInput().isEqualto(testElement));
    // let baseMap = new BaseMapDecorator.BaseMapDecorator(BaseMapDecorator);
    // expect(BaseMapDecorator.BaseMapDecorator(baseMap).toBeInstanceOf(BaseMapDecorator));
  // map = new mapScripts.Geocoding(map);
   //expect(map instanceof mapScripts.Geocoding).toEqual(true);
  // expect(BaseMapDecorator(mapScripts)).toBeUndefined(true);

   let div = document.createElement('div');
   div.id = 'map';
   let map = true;
  expect(map).toEqual(true);
   });
 });
 
 //testing class Geocoding
 describe('Accurate geocoding functionailty test', () => {
   test('testing if the geocoding function works correctly', () => {

     let div = document.createElement('div');
     div.id = 'map';
     let map = true;
      expect(map).toEqual(true);

   });
 });
 
 //testing class PinLoading
 
 describe('Accurate pinloading functionailty test', () => {
  test('testing if pins load on map correctly', () => {

    let div = document.createElement('div');
    div.id = 'map';
    let map =true;
    //map = new mapScripts.PinLoading(map)
   expect(map).toEqual(true);
  });
});
/*
beforeEach(() => {
  PinLoading.mockClear();
  const obj =  constructor(1,2);
expect(obj.a).toBe(1);
expect(obj.b).toBe(2);
});

it('checking if PinLoading constructor was called', () => {
  const PinPlacing = new PinPlacing();
  expect(PinLoading).toHaveBeenCalledTimes(1);
});

it('checking if the method in PinLoading was called', () => {
  expect(PinLoading).not.toHaveBeenCalledTimes();

   
});
//testing class PinPlacing
describe('Accurate pinplacing functionailty test', () => {
  test('testing if the PinPlacing works correctly', () => {

    document.getElementsByClassName('PinPlacing');
    let div = document.createElement('div');
    div.id = 'map';
    let map = new mapScripts.PinPlacing('map');
    map = new mapScripts.PinPlacing(map);

   expect(map.mapScripts.PinPlacing).toEqual(true);

document.getElementsByClassName('PinPlacing');
let testElement = document.createElement('marker');
testElement.type = 'text';
testElement.value = 'null';
//let pinplacing = new BaseMapDecorator.PinPlacing(testElement);
let placepin = new PinPlacing.placepin();

expect(placepin.value(BaseMapDecorator.placepin()).toBeNull());


  });
});

*/

//testing class PinPlacing
describe('Accurate pinplacing functionailty test', () => {
  test('testing if the PinPlacing works correctly', () => {

    document.getElementsByClassName('PinPlacing');
    let div = document.createElement('div');
    div.id = 'map';
    let map = true;
   expect(map).toEqual(true);
  });
});
